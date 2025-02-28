"""
Routes and view functions for the Flask Selenium Testing Framework
"""

import os
import json
import threading
import uuid
import inspect
import importlib.util
import concurrent.futures
import logging
from flask import request, jsonify, render_template, send_from_directory

from config import Config
from test_runner import TestRunner
from utils.logger import Logger

# Setup logging
logger = Logger(__name__)

# Store test results in memory
test_results = {}
active_tests = {}
test_executors = {}  # Store executor instances for parallel tests

def register_routes(app):
    """
    Register all application routes
    """
    # Main routes
    @app.route('/')
    def index():
        """
        Render the main dashboard
        """
        return render_template('index.html')
    
    @app.route('/screenshots/<path:filename>')
    def serve_screenshot(filename):
        """
        Serve a screenshot file
        """
        return send_from_directory('screenshots', filename)
    
    # API routes for test management
    register_test_api_routes(app)

def register_test_api_routes(app):
    """
    Register API routes for test management
    """
    @app.route('/api/tests', methods=['GET'])
    def get_tests():
        """
        Get a list of available tests
        """
        tests_dir = os.path.join(os.getcwd(), 'tests')
        tests = []
        
        for root, _, files in os.walk(tests_dir):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    rel_path = os.path.relpath(os.path.join(root, file), tests_dir)
                    tests.append({
                        'path': rel_path,
                        'name': os.path.splitext(rel_path)[0]
                    })
        
        return jsonify(tests)
    
    @app.route('/api/test_functions', methods=['GET'])
    def get_test_functions():
        """
        Get a list of test functions in a test file
        """
        test_path = request.args.get('path')
        
        if not test_path:
            return jsonify({'error': 'No test path provided'}), 400
        
        full_path = os.path.join(os.getcwd(), 'tests', test_path)
        
        if not os.path.isfile(full_path):
            return jsonify({'error': f'Test file not found: {test_path}'}), 404
        
        try:
            # Import the test module
            module_name = os.path.basename(test_path).replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find all test functions
            test_functions = []
            for name, obj in inspect.getmembers(module):
                if name.startswith('test_') and callable(obj):
                    test_functions.append(name)
            
            return jsonify(test_functions)
        except Exception as e:
            logger.error(f"Error loading test functions from {test_path}: {str(e)}")
            return jsonify({'error': f'Error loading test functions: {str(e)}'}), 500
    
    @app.route('/api/run', methods=['POST'])
    def run_test():
        """
        Run a test or a directory of tests, optionally with specific functions
        """
        data = request.json
        test_path = data.get('path')
        browser_type = data.get('browser', 'chrome')
        headless_mode = data.get('headless', False)
        functions = data.get('functions', [])  # List of function names to run
        
        if not test_path:
            return jsonify({'error': 'No test path provided'}), 400
        
        # Create a unique ID for this test run
        run_id = str(uuid.uuid4())
        
        # Start the test in a separate thread
        def run_test_thread():
            config = Config()
            # Override headless mode from request
            config.HEADLESS = headless_mode
            runner = TestRunner(config)
            active_tests[run_id] = runner
            
            try:
                full_path = os.path.join(os.getcwd(), 'tests', test_path)
                
                # Import the test module
                module_name = os.path.basename(test_path).replace('.py', '')
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Set up the test environment
                runner.setup(browser_type)
                
                try:
                    results = {
                        'total': 0,
                        'passed': 0,
                        'failed': 0,
                        'skipped': 0,
                        'tests': []
                    }
                    
                    # Run specific test functions if provided, otherwise run all
                    test_functions = []
                    if functions:
                        for func_name in functions:
                            if hasattr(module, func_name) and callable(getattr(module, func_name)):
                                test_functions.append(getattr(module, func_name))
                    else:
                        for name, obj in inspect.getmembers(module):
                            if name.startswith('test_') and callable(obj):
                                test_functions.append(obj)
                    
                    # Run each function
                    for func in test_functions:
                        result = runner.run_test(func)
                        results['total'] += 1
                        if result['status'] == 'passed':
                            results['passed'] += 1
                        elif result['status'] == 'failed':
                            results['failed'] += 1
                        else:
                            results['skipped'] += 1
                        
                        results['tests'].append(result)
                    
                    # Store the results
                    test_results[run_id] = results
                    
                    logger.info(f"Test run {run_id} completed")
                finally:
                    # Always clean up
                    runner.teardown()
            except Exception as e:
                logger.error(f"Error running test {run_id}: {str(e)}")
                test_results[run_id] = {
                    'error': str(e),
                    'status': 'error'
                }
            finally:
                # Clean up
                if run_id in active_tests:
                    del active_tests[run_id]
        
        thread = threading.Thread(target=run_test_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'run_id': run_id,
            'status': 'started'
        })
    
    @app.route('/api/results/<run_id>', methods=['GET'])
    def get_results(run_id):
        """
        Get the results of a test run, including in-progress results
        """
        if run_id in test_results:
            # Test completed
            return jsonify({
                'status': 'completed',
                'results': test_results[run_id]
            })
        elif run_id in active_tests:
            # Test is still running, get partial results
            runner = active_tests[run_id]
            partial_results = getattr(runner, 'results', {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'tests': []
            })
            
            return jsonify({
                'status': 'running',
                'results': partial_results
            })
        else:
            return jsonify({
                'status': 'not_found'
            }), 404
    
    @app.route('/api/stop/<run_id>', methods=['POST'])
    def stop_test(run_id):
        """
        Stop a running test
        """
        if run_id in active_tests:
            try:
                # Try to tear down the test runner
                active_tests[run_id].teardown()
                del active_tests[run_id]
                return jsonify({'status': 'stopped'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            return jsonify({'status': 'not_found'}), 404
    
    @app.route('/api/run_parallel', methods=['POST'])
    def run_tests_parallel():
        """
        Run multiple tests in parallel
        """
        data = request.json
        test_paths = data.get('paths', [])
        browser_type = data.get('browser', 'chrome')
        headless_mode = data.get('headless', False)
        max_workers = data.get('max_workers', 3)  # Default to 3 parallel workers
        test_functions = data.get('test_functions', {})  # Dictionary of selected functions per test
        
        if not test_paths or not isinstance(test_paths, list):
            return jsonify({'error': 'No test paths provided or invalid format'}), 400
        
        # Create a unique ID for this parallel test run
        parallel_run_id = str(uuid.uuid4())
        
        # Create a thread to manage parallel execution
        def run_parallel_tests_thread():
            try:
                # Create a ThreadPoolExecutor for parallel execution
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
                test_executors[parallel_run_id] = executor
                
                # Store combined results
                combined_results = {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'tests': [],
                    'test_files': {},
                    'status': 'running'
                }
                test_results[parallel_run_id] = combined_results
                
                # Function to run a single test file
                def run_test_file(test_path):
                    # Create a unique ID for this individual test
                    run_id = f"{parallel_run_id}_{test_path.replace('/', '_').replace('.', '_')}"
                    
                    try:
                        config = Config()
                        config.HEADLESS = headless_mode
                        runner = TestRunner(config)
                        active_tests[run_id] = runner
                        
                        # Store initial status in combined results immediately
                        combined_results['test_files'][test_path] = {
                            'run_id': run_id,
                            'status': 'running',
                            'total': 0,
                            'passed': 0,
                            'failed': 0
                        }
                        
                        full_path = os.path.join(os.getcwd(), 'tests', test_path)
                        
                        # Set up test environment
                        runner.setup(browser_type)
                        
                        try:
                            # Import the test module
                            module_name = os.path.basename(test_path).replace('.py', '')
                            spec = importlib.util.spec_from_file_location(module_name, full_path)
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            
                            # Find all test functions - respect selected functions if any
                            test_functions_to_run = []
                            selected_funcs = test_functions.get(test_path, [])
                            
                            for name, obj in inspect.getmembers(module):
                                if name.startswith('test_') and callable(obj):
                                    # If specific functions are selected, only run those
                                    if not selected_funcs or name in selected_funcs:
                                        test_functions_to_run.append(obj)
                            
                            # Update total count in combined results
                            combined_results['test_files'][test_path]['total'] = len(test_functions_to_run)
                            
                            # Initialize results
                            results = {
                                'total': len(test_functions_to_run),
                                'passed': 0,
                                'failed': 0,
                                'skipped': 0,
                                'tests': []
                            }
                            
                            # Run each test function
                            for func in test_functions_to_run:
                                # Run the test and get result
                                result = runner.run_test(func)
                                
                                # Update combined results after each test
                                if result['status'] == 'passed':
                                    combined_results['test_files'][test_path]['passed'] += 1
                                elif result['status'] == 'failed':
                                    combined_results['test_files'][test_path]['failed'] += 1
                                
                                # Add the result to the test's results
                                results['tests'].append(result)
                                
                                # Also add to combined results with test path information
                                test_result = result.copy()
                                test_result['test_path'] = test_path
                                test_result['run_id'] = run_id
                                combined_results['tests'].append(test_result)
                            
                            # Update final counts
                            results['passed'] = sum(1 for t in results['tests'] if t['status'] == 'passed')
                            results['failed'] = sum(1 for t in results['tests'] if t['status'] == 'failed')
                            results['skipped'] = results['total'] - results['passed'] - results['failed']
                            
                            # Store results
                            test_results[run_id] = results
                            
                            # Update status in combined results
                            combined_results['test_files'][test_path]['status'] = 'completed'
                            
                            logger.info(f"Test run {run_id} completed")
                            
                            return {
                                'run_id': run_id,
                                'path': test_path,
                                'results': results
                            }
                        finally:
                            # Clean up
                            runner.teardown()
                            if run_id in active_tests:
                                del active_tests[run_id]
                    except Exception as e:
                        logger.error(f"Error running test {run_id}: {str(e)}")
                        
                        # Update status in combined results
                        if test_path in combined_results['test_files']:
                            combined_results['test_files'][test_path]['status'] = 'error'
                            combined_results['test_files'][test_path]['error'] = str(e)
                        
                        test_results[run_id] = {
                            'error': str(e),
                            'status': 'error'
                        }
                        
                        return {
                            'run_id': run_id,
                            'path': test_path,
                            'error': str(e),
                            'status': 'error'
                        }
                
                # Submit all test files to the executor
                future_to_test = {executor.submit(run_test_file, test_path): test_path 
                                for test_path in test_paths}
                
                # Process results as they complete
                for future in concurrent.futures.as_completed(future_to_test):
                    test_path = future_to_test[future]
                    try:
                        result = future.result()
                        
                        if 'results' in result:
                            # Update combined stats
                            file_results = result['results']
                            combined_results['total'] += file_results['total']
                            combined_results['passed'] += file_results['passed']
                            combined_results['failed'] += file_results['failed']
                            combined_results['skipped'] += file_results['skipped']
                        else:
                            # Handle error case
                            combined_results['test_files'][test_path] = {
                                'run_id': result['run_id'],
                                'status': 'error',
                                'error': result.get('error', 'Unknown error')
                            }
                    except Exception as e:
                        logger.error(f"Error processing results for {test_path}: {str(e)}")
                        combined_results['test_files'][test_path] = {
                            'status': 'error',
                            'error': str(e)
                        }
                
                # Mark as completed
                combined_results['status'] = 'completed'
                
                logger.info(f"Parallel test run {parallel_run_id} completed")
            except Exception as e:
                logger.error(f"Error in parallel test execution {parallel_run_id}: {str(e)}")
                test_results[parallel_run_id] = {
                    'error': str(e),
                    'status': 'error'
                }
            finally:
                # Clean up
                if parallel_run_id in test_executors:
                    test_executors[parallel_run_id].shutdown(wait=False)
                    del test_executors[parallel_run_id]
        
        # Start parallel execution in a separate thread
        thread = threading.Thread(target=run_parallel_tests_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'parallel_run_id': parallel_run_id,
            'status': 'started',
            'test_count': len(test_paths)
        })

        
    @app.route('/api/parallel_results/<parallel_run_id>', methods=['GET'])
    def get_parallel_results(parallel_run_id):
        """
        Get the results of a parallel test run
        """
        if parallel_run_id in test_results:
            return jsonify({
                'status': test_results[parallel_run_id].get('status', 'completed'),
                'results': test_results[parallel_run_id]
            })
        elif parallel_run_id in test_executors:
            return jsonify({
                'status': 'running'
            })
        else:
            return jsonify({
                'status': 'not_found'
            }), 404

    @app.route('/api/stop_parallel/<parallel_run_id>', methods=['POST'])
    def stop_parallel_tests(parallel_run_id):
        """
        Stop a running parallel test execution
        """
        if parallel_run_id in test_executors:
            try:
                # Shut down the executor
                test_executors[parallel_run_id].shutdown(wait=False)
                del test_executors[parallel_run_id]
                
                # Clean up any active tests
                for run_id in list(active_tests.keys()):
                    if run_id.startswith(f"{parallel_run_id}_"):
                        try:
                            active_tests[run_id].teardown()
                            del active_tests[run_id]
                        except Exception as e:
                            logger.error(f"Error cleaning up test {run_id}: {str(e)}")
                
                return jsonify({'status': 'stopped'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            return jsonify({'status': 'not_found'}), 404
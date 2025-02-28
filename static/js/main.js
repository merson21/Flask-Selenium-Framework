document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const testList = document.querySelector('.test-list');
    const functionList = document.getElementById('function-list');
    const testFunctions = document.getElementById('test-functions');
    const runAllFunctions = document.getElementById('run-all-functions');
    const runSelectedBtn = document.getElementById('run-selected-btn');
    const statusBadge = document.getElementById('status-badge');
    const noResultsMessage = document.getElementById('no-results-message');
    const totalTests = document.getElementById('total-tests');
    const passedTests = document.getElementById('passed-tests');
    const failedTests = document.getElementById('failed-tests');
    const testLogs = document.getElementById('test-logs');
    const headlessMode = document.getElementById('headless-mode');
    const maxWorkers = document.getElementById('max-workers');
    const executionMode = document.getElementById('execution-mode');
    const detailedResultsContainer = document.getElementById('detailed-results-container');
    
    // Error modal elements
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    const errorMessage = document.getElementById('error-message');
    const errorScreenshot = document.getElementById('error-screenshot');
    const screenshotContainer = document.getElementById('screenshot-container');

    // State variables
    const selectedTests = new Set();
    let selectedTestFile = null;
    let currentRunId = null;
    let selectedFunctions = new Set();
    let testExecutionMode = 'single'; // 'single' or 'parallel'
    // To store selected functions per test file
    const selectedFunctionsByTest = {};
    
    /**
     * Updates the execution mode based on selected tests
     */
    function updateExecutionMode() {
        if (selectedTests.size === 0) {
            executionMode.textContent = 'Select tests to run';
            runSelectedBtn.disabled = true;
            testExecutionMode = 'single';
        } else if (selectedTests.size === 1) {
            executionMode.textContent = 'Mode: Single Test Execution';
            runSelectedBtn.disabled = false;
            testExecutionMode = 'single';
        } else {
            executionMode.textContent = `Mode: Parallel Execution (${selectedTests.size} tests)`;
            runSelectedBtn.disabled = false;
            testExecutionMode = 'parallel';
        }
    }
    
    /**
     * Fetches available tests and populates the test list
     */
    function fetchTests() {
        fetch('/api/tests')
            .then(response => response.json())
            .then(tests => {
                testList.innerHTML = '';
                
                if (tests.length === 0) {
                    testList.innerHTML = '<div class="text-center text-muted"><p>No tests found</p></div>';
                    return;
                }
                
                tests.forEach(test => {
                    const listItem = document.createElement('div');
                    listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');
                    listItem.dataset.path = test.path;
                    listItem.dataset.name = test.name;
                    
                    // Test name with checkbox for multiple selection
                    listItem.innerHTML = `
                        <div class="form-check">
                            <input class="form-check-input test-checkbox" type="checkbox" id="test-${test.name}" data-path="${test.path}">
                            <label class="form-check-label" for="test-${test.name}">
                                ${test.name}
                            </label>
                        </div>
                        <button class="btn btn-sm btn-outline-primary view-functions-btn">View Functions</button>
                    `;
                    
                    // Add click handler for test selection
                    const checkbox = listItem.querySelector('.test-checkbox');
                    checkbox.addEventListener('change', function() {
                        if (this.checked) {
                            selectedTests.add(this.dataset.path);
                        } else {
                            selectedTests.delete(this.dataset.path);
                        }
                        
                        updateExecutionMode();
                    });
                    
                    // Add click handler for viewing functions
                    const viewFunctionsBtn = listItem.querySelector('.view-functions-btn');
                    viewFunctionsBtn.addEventListener('click', function(e) {
                        e.preventDefault();
                        
                        const testPath = this.closest('.list-group-item').dataset.path;
                        selectedTestFile = testPath;
                        
                        // Fetch test functions for this file
                        fetchTestFunctions(testPath);
                    });
                    
                    testList.appendChild(listItem);
                });
            })
            .catch(error => {
                console.error('Error fetching tests:', error);
                testList.innerHTML = '<div class="text-center text-danger"><p>Error loading tests</p></div>';
            });
    }
    
    /**
     * Fetches test functions for a specific file
     * @param {string} testPath - Path to the test file
     */
    function fetchTestFunctions(testPath) {
        // Show the function list section
        functionList.style.display = 'block';
        
        // Clear current functions display
        testFunctions.innerHTML = '';
        
        // Initialize or get the selected functions set for this test
        if (!selectedFunctionsByTest[testPath]) {
            selectedFunctionsByTest[testPath] = new Set();
        }
        selectedFunctions = selectedFunctionsByTest[testPath];
        
        // Make API call to get functions
        fetch(`/api/test_functions?path=${encodeURIComponent(testPath)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(functions => {
                console.log("Fetched functions:", functions); // Debug log
                
                if (!Array.isArray(functions) || functions.length === 0) {
                    testFunctions.innerHTML = '<div class="text-center text-muted"><p>No test functions found</p></div>';
                    return;
                }
                
                // Reset "Run All" checkbox based on this test's selected functions
                runAllFunctions.checked = selectedFunctions.size === 0 || selectedFunctions.size === functions.length;
                
                functions.forEach(func => {
                    const functionItem = document.createElement('div');
                    functionItem.classList.add('form-check');
                    
                    functionItem.innerHTML = `
                        <input class="form-check-input function-checkbox" type="checkbox" id="func-${func}" 
                               data-function="${func}" ${runAllFunctions.checked || selectedFunctions.has(func) ? 'checked' : ''}>
                        <label class="form-check-label" for="func-${func}">
                            ${func}
                        </label>
                    `;
                    
                    testFunctions.appendChild(functionItem);
                    
                    if (runAllFunctions.checked && !selectedFunctions.has(func)) {
                        selectedFunctions.add(func);
                    }
                });
                
                // Add event listeners to function checkboxes
                document.querySelectorAll('.function-checkbox').forEach(checkbox => {
                    checkbox.addEventListener('change', function() {
                        if (this.checked) {
                            selectedFunctions.add(this.dataset.function);
                        } else {
                            selectedFunctions.delete(this.dataset.function);
                        }
                        
                        // If all are selected, check the "Run All" checkbox
                        const allCheckboxes = document.querySelectorAll('.function-checkbox');
                        const allChecked = Array.from(allCheckboxes).every(cb => cb.checked);
                        runAllFunctions.checked = allChecked;
                    });
                });
                
                // Make sure function list is visible
                console.log("Function list should be displayed:", functionList.style.display);
            })
            .catch(error => {
                console.error('Error fetching test functions:', error);
                testFunctions.innerHTML = '<div class="text-center text-danger"><p>Error loading test functions: ' + error.message + '</p></div>';
            });
    }
    
    /**
     * Polls for test results
     * @param {string} runId - ID of the test run
     */
    function pollResults(runId) {
        if (!runId) {
            console.error("Invalid runId:", runId);
            testLogs.textContent += "Error: Invalid test run ID\n";
            return;
        }
        
        const interval = setInterval(() => {
            fetch(`/api/results/${runId}`)
                .then(response => {
                    if (!response.ok) {
                        if (response.status === 404) {
                            console.warn(`Test run ${runId} not found yet, waiting...`);
                            return { status: 'waiting' };
                        }
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'waiting') {
                        // Do nothing, just wait for the next poll
                        return;
                    }
                    
                    // Handle in-progress results
                    if (data.status === 'running' && data.results) {
                        // Update summary counters with current progress
                        const results = data.results;
                        totalTests.textContent = results.total || 0;
                        passedTests.textContent = results.passed || 0;
                        failedTests.textContent = results.failed || 0;
                        
                        // Create test table if it doesn't exist
                        const testName = selectedTestFile.split('/').pop().replace('.py', '');
                        const tableId = createTestTable(testName, selectedTestFile);
                        
                        // Update test table status
                        updateTestTableStatus(tableId, 'running', 
                            results.passed + results.failed, 
                            results.total);
                        
                        // Process each test result
                        results.tests.forEach(test => {
                            // Extract function name - improved to avoid duplicates
                            let funcName = test.name;
                            
                            // Only take the part after the last dot if it contains a dot
                            if (funcName.includes('.')) {
                                funcName = funcName.substring(funcName.lastIndexOf('.') + 1);
                            }
                            
                            // Remove 'test_' prefix if it exists
                            if (funcName.startsWith('test_')) {
                                funcName = funcName.substring(5);
                            }
                            
                            // Add/update function row
                            const rowId = addFunctionRow(tableId, funcName);
                            updateFunctionStatus(rowId, test.status, test.error);
                        });
                    }
                    // Handle completed results
                    else if (data.status === 'completed') {
                        clearInterval(interval);
                        
                        // Update logs
                        testLogs.textContent += `Test run ${runId} completed\n`;
                        
                        // Update summary counters
                        const results = data.results;
                        totalTests.textContent = results.total;
                        passedTests.textContent = results.passed;
                        failedTests.textContent = results.failed;
                        
                        // Create/update test table
                        const testName = selectedTestFile.split('/').pop().replace('.py', '');
                        const tableId = createTestTable(testName, selectedTestFile);
                        
                        // Update test table status
                        const status = results.failed > 0 ? 'failed' : 'passed';
                        updateTestTableStatus(tableId, status, results.total, results.total);
                        
                        // Process each test result
                        results.tests.forEach(test => {
                            // Extract function name - improved to avoid duplicates
                            let funcName = test.name;
                            
                            // Only take the part after the last dot if it contains a dot
                            if (funcName.includes('.')) {
                                funcName = funcName.substring(funcName.lastIndexOf('.') + 1);
                            }
                            
                            // Remove 'test_' prefix if it exists
                            if (funcName.startsWith('test_')) {
                                funcName = funcName.substring(5);
                            }
                            
                            // Add/update function row
                            const rowId = addFunctionRow(tableId, funcName);
                            updateFunctionStatus(rowId, test.status, test.error);
                        });
                        
                        // Update status
                        statusBadge.textContent = 'Completed';
                        statusBadge.className = 'badge bg-success';
                        
                        // Auto-scroll logs to bottom
                        testLogs.scrollTop = testLogs.scrollHeight;
                    }
                })
                .catch(error => {
                    console.error('Error polling results:', error);
                    testLogs.textContent += `Error polling results for run ${runId}: ${error.message}\n`;
                    clearInterval(interval);
                });
        }, 500); // Poll every 500ms for more responsive updates
    }
    
    /**
     * Polls for parallel test results
     * @param {string} parallelRunId - ID of the parallel test run
     */
    function pollParallelResults(parallelRunId) {
        // Keep track of created tables
        const testTables = {};
        
        // Reduce polling interval for more responsive updates
        const interval = setInterval(() => {
            fetch(`/api/parallel_results/${parallelRunId}`)
                .then(response => response.json())
                .then(data => {
                    // Update summary counters if available
                    if (data.results) {
                        if (data.results.total !== undefined) totalTests.textContent = data.results.total || 0;
                        if (data.results.passed !== undefined) passedTests.textContent = data.results.passed || 0;
                        if (data.results.failed !== undefined) failedTests.textContent = data.results.failed || 0;
                        
                        // Process test files (test-level updates)
                        if (data.results.test_files) {
                            for (const [testPath, testResult] of Object.entries(data.results.test_files)) {
                                const testName = testPath.split('/').pop().replace('.py', '');
                                let tableId = testTables[testPath];
                                
                                // Create table if it doesn't exist yet
                                if (!tableId) {
                                    tableId = createTestTable(testName, testPath);
                                    testTables[testPath] = tableId;
                                }
                                
                                // Update table status based on current state
                                if (testResult.status === 'running') {
                                    const completed = (testResult.passed || 0) + (testResult.failed || 0);
                                    const total = testResult.total || 1;
                                    updateTestTableStatus(tableId, 'running', completed, total);
                                } else if (testResult.status === 'completed') {
                                    const status = (testResult.failed || 0) > 0 ? 'failed' : 'passed';
                                    updateTestTableStatus(tableId, status, testResult.total, testResult.total);
                                } else if (testResult.status === 'error') {
                                    updateTestTableStatus(tableId, 'failed', 0, 0);
                                    // Add error message to table
                                    const errorRow = addFunctionRow(tableId, "Error running test");
                                    updateFunctionStatus(errorRow, 'failed', testResult.error || 'Unknown error');
                                }
                            }
                        }
                        
                        // Process individual test functions (function-level updates)
                        if (data.results.tests) {
                            data.results.tests.forEach(test => {
                                // Find which test file this test belongs to
                                let testPath = test.test_path;
                                if (!testPath) {
                                    // Try to determine test path from result data
                                    for (const [path, fileResult] of Object.entries(data.results.test_files)) {
                                        if (fileResult.run_id === test.run_id || test.name.includes(path)) {
                                            testPath = path;
                                            break;
                                        }
                                    }
                                }
                                
                                if (testPath) {
                                    // Get table for this test
                                    const testName = testPath.split('/').pop().replace('.py', '');
                                    let tableId = testTables[testPath];
                                    
                                    // Should have been created in the test file loop, but just in case
                                    if (!tableId) {
                                        tableId = createTestTable(testName, testPath);
                                        testTables[testPath] = tableId;
                                    }
                                    
                                    // Extract function name from test name
                                    let funcName = test.name;
                                    if (funcName.includes(testName)) {
                                        funcName = funcName.substring(funcName.indexOf(testName) + testName.length + 1);
                                    } else if (funcName.startsWith('test_')) {
                                        funcName = funcName.substring(5);
                                    }
                                    
                                    // Add/update function row
                                    const rowId = addFunctionRow(tableId, funcName);
                                    updateFunctionStatus(rowId, test.status, test.error);
                                }
                            });
                        }
                    }
                    
                    // Handle completed state
                    if (data.status === 'completed') {
                        clearInterval(interval);
                        
                        // Update overall status
                        statusBadge.textContent = 'Completed';
                        statusBadge.className = 'badge bg-success';
                        
                        // Final update to logs
                        testLogs.textContent += `Parallel test run ${parallelRunId} completed\n`;
                    } 
                    // Handle running updates
                    else if (data.status === 'running') {
                        // Update progress indicator if we have test files info
                        if (data.results && data.results.test_files) {
                            const fileStatus = Object.values(data.results.test_files);
                            const completed = fileStatus.filter(f => f.status === 'completed').length;
                            const total = Object.keys(data.results.test_files).length;
                            
                            statusBadge.textContent = `Running (${completed}/${total})`;
                            
                            // Update logs occasionally to avoid flooding
                            if (completed > 0 && completed % 2 === 0) {
                                testLogs.textContent += `Progress: ${completed}/${total} test files completed\n`;
                                
                                // Auto-scroll logs to bottom
                                testLogs.scrollTop = testLogs.scrollHeight;
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error('Error polling parallel results:', error);
                    testLogs.textContent += `Error polling parallel results for run ${parallelRunId}: ${error.message}\n`;
                    clearInterval(interval);
                });
        }, 500); // Poll every 500ms for more responsive updates
    }
    
    /**
     * Resets the results display and prepares for a test run
     */
    function resetResultsDisplay() {
        statusBadge.textContent = 'Running';
        statusBadge.className = 'badge bg-warning';
        noResultsMessage.style.display = 'none';
        detailedResultsContainer.innerHTML = '';
        testLogs.textContent = 'Starting test execution...\n';
        totalTests.textContent = '0';
        passedTests.textContent = '0';
        failedTests.textContent = '0';
    }
    
    /**
     * Runs a single test
     * @param {string} testPath - Path to the test file
     * @param {Array} functions - Array of function names to run
     */
    function runSingleTest(testPath, functions) {
        // If no specific functions are provided, get them from our stored selection
        if (!functions || functions.length === 0) {
            if (selectedFunctionsByTest[testPath] && selectedFunctionsByTest[testPath].size > 0) {
                functions = Array.from(selectedFunctionsByTest[testPath]);
            } else {
                functions = [];
            }
        }
        
        fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                path: testPath,
                browser: document.getElementById('browser-select').value,
                headless: document.getElementById('headless-mode').checked,
                functions: functions
            })
        })
        .then(response => response.json())
        .then(data => {
            currentRunId = data.run_id;
            testLogs.textContent += `Started test run ${data.run_id} for ${testPath}\n`;
            
            if (functions.length > 0) {
                testLogs.textContent += `Running functions: ${functions.join(', ')}\n`;
            }
            
            // Create test table and mark as running
            const testName = testPath.split('/').pop().replace('.py', '');
            const tableId = createTestTable(testName, testPath);
            updateTestTableStatus(tableId, 'running', 0, functions.length || 1);
            
            // If specific functions are selected, create rows for them
            if (functions.length > 0) {
                functions.forEach(func => {
                    const rowId = addFunctionRow(tableId, func);
                    updateFunctionStatus(rowId, 'running');
                });
            } else {
                // Otherwise, create a generic row to show something is happening
                const rowId = addFunctionRow(tableId, "Running all tests...");
                updateFunctionStatus(rowId, 'running');
            }
            
            // Auto-scroll logs to bottom
            testLogs.scrollTop = testLogs.scrollHeight;
            
            // Poll for results
            pollResults(data.run_id);
        })
        .catch(error => {
            console.error('Error starting test:', error);
            testLogs.textContent += `Error starting test ${testPath}: ${error.message}\n`;
            
            // Create error table
            const testName = testPath.split('/').pop().replace('.py', '');
            const tableId = createTestTable(testName, testPath);
            updateTestTableStatus(tableId, 'failed', 0, 1);
            
            // Add error row
            const rowId = addFunctionRow(tableId, "Error starting test");
            updateFunctionStatus(rowId, 'failed', error.message);
            
            // Auto-scroll logs to bottom
            testLogs.scrollTop = testLogs.scrollHeight;
        });
    }
    
    /**
     * Runs tests in parallel
     * @param {Array} testPaths - Array of test paths to run
     */
    function runParallelTests(testPaths) {
        const maxWorkersValue = Math.min(parseInt(maxWorkers.value, 10), testPaths.length);
        
        // Create a dictionary of selected functions for each test path
        const testFunctionsDict = {};
        testPaths.forEach(testPath => {
            if (selectedFunctionsByTest[testPath] && selectedFunctionsByTest[testPath].size > 0) {
                testFunctionsDict[testPath] = Array.from(selectedFunctionsByTest[testPath]);
            }
        });
        
        fetch('/api/run_parallel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                paths: testPaths,
                browser: document.getElementById('browser-select').value,
                headless: document.getElementById('headless-mode').checked,
                max_workers: maxWorkersValue,
                test_functions: testFunctionsDict  // Send selected functions
            })
        })
        .then(response => response.json())
        .then(data => {
            const parallelRunId = data.parallel_run_id;
            testLogs.textContent += `Started parallel test run ${parallelRunId} with ${data.test_count} tests\n`;
            testLogs.textContent += `Maximum parallel workers: ${maxWorkersValue}\n`;
            
            // Create tables for all tests and mark as pending
            testPaths.forEach(testPath => {
                const testName = testPath.split('/').pop().replace('.py', '');
                const tableId = createTestTable(testName, testPath);
                updateTestTableStatus(tableId, 'pending');
                
                // If specific functions are selected for this test, show them
                if (testFunctionsDict[testPath]) {
                    testFunctionsDict[testPath].forEach(func => {
                        // Normalize function name
                        let normalizedFunc = func;
                        if (normalizedFunc.startsWith('test_')) {
                            normalizedFunc = normalizedFunc.substring(5);
                        }
                        
                        const rowId = addFunctionRow(tableId, normalizedFunc);
                        updateFunctionStatus(rowId, 'pending');
                    });
                }
            });
            
            // Auto-scroll logs to bottom
            testLogs.scrollTop = testLogs.scrollHeight;
            
            // Poll for parallel results
            pollParallelResults(parallelRunId);
        })
        .catch(error => {
            console.error('Error starting parallel tests:', error);
            testLogs.textContent += `Error starting tests: ${error.message}\n`;
            
            // Show error in tables
            testPaths.forEach(testPath => {
                const testName = testPath.split('/').pop().replace('.py', '');
                const tableId = createTestTable(testName, testPath);
                updateTestTableStatus(tableId, 'failed', 0, 1);
                
                // Add error row
                const rowId = addFunctionRow(tableId, "Error starting test");
                updateFunctionStatus(rowId, 'failed', error.message);
            });
            
            // Auto-scroll logs to bottom
            testLogs.scrollTop = testLogs.scrollHeight;
        });
    }
    
    // Event Listeners
    
    // Run All Functions checkbox handler
    runAllFunctions.addEventListener('change', function() {
        // Get the current test path
        if (!selectedTestFile) return;
        
        // Make sure we have a set for this test
        if (!selectedFunctionsByTest[selectedTestFile]) {
            selectedFunctionsByTest[selectedTestFile] = new Set();
        }
        selectedFunctions = selectedFunctionsByTest[selectedTestFile];
        
        const functionCheckboxes = document.querySelectorAll('.function-checkbox');
        
        functionCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
            
            if (this.checked) {
                selectedFunctions.add(checkbox.dataset.function);
            } else {
                selectedFunctions.delete(checkbox.dataset.function);
            }
        });
    });
    
    
    
    // Select/deselect all tests buttons
    document.getElementById('select-all-tests').addEventListener('click', function() {
        document.querySelectorAll('.test-checkbox').forEach(checkbox => {
            checkbox.checked = true;
            selectedTests.add(checkbox.dataset.path);
        });
        updateExecutionMode();
    });
    
    document.getElementById('deselect-all-tests').addEventListener('click', function() {
        document.querySelectorAll('.test-checkbox').forEach(checkbox => {
            checkbox.checked = false;
            selectedTests.delete(checkbox.dataset.path);
        });
        updateExecutionMode();
        
        // Hide function list when deselecting all
        functionList.style.display = 'none';
    });
    
    // Run selected tests button handler
    runSelectedBtn.addEventListener('click', function() {
        if (selectedTests.size === 0) return;
        
        resetResultsDisplay();
        
        // Single test execution
        if (testExecutionMode === 'single') {
            // Get the selected test path (first one in the set)
            const testPath = Array.from(selectedTests)[0];
            runSingleTest(testPath);
        }
        // Parallel test execution
        else {
            runParallelTests(Array.from(selectedTests));
        }
    });
    
    // Initialize
    fetchTests();
    updateExecutionMode();
});
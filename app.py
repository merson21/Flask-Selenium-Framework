"""
Main application file for the Flask Selenium Testing Framework
"""

import os
import logging
from flask import Flask

from config import Config
from routes import register_routes

def create_app(config_class=Config):
    """
    Application factory function to create and configure the Flask app
    """
    # Initialize Flask app
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join('logs', 'app.log')),
            logging.StreamHandler()
        ]
    )
    
    # Create required directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('screenshots', exist_ok=True)
    
    # Register all routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
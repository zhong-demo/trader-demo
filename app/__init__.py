from flask import Flask
from .routes import main
from .logging_config import setup_logging
from .scheduler import start_scheduler

def create_app():
    app = Flask(__name__)
    
    # Set up logging
    setup_logging()
    
    # Register blueprint
    app.register_blueprint(main)
    
    # Start the scheduler
    with app.app_context():
        start_scheduler()
    
    return app

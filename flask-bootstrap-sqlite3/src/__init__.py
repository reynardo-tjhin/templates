import os

from flask import Flask
from flask_wtf import CSRFProtect

# load the configuration
# config.py file will first load configuration from .env file
from .config import config
from . import routes

# initialise CSRF object for secure post method
csrf = CSRFProtect()

def create_app():
    """
    Create and configure an instance of the Flask application.
    """
    # determine the config based on environment variable
    config_name = os.getenv('FLASK_ENV', 'development')

    # create the app object
    app = Flask(__name__)

    # update the configuration
    cfg = config[config_name] # returns a 'Config' object
    app.config.from_object(cfg)

    # update the database instance path
    # the app.instance_path is based on where the parent folder of the app is
    # for e.g. '%app_path%/instance/src.sqlite'
    app.config.update(DATABASE=os.path.join(app.instance_path, 'src.sqlite'))

    # we need to create an 'instance' folder if it does not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register blueprints
    app.register_blueprint(routes.bp)

    return app

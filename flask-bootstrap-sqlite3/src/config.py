import os
import configparser

from pathlib import Path
from dotenv import load_dotenv

# load the environment variables
env_path = Path(__file__).parent.parent / 'example.env'
load_dotenv(env_path)

# initialise the configuration for the app
cfg = configparser.ConfigParser()
cfg_path = Path(__file__).parent.parent / 'config.ini'
cfg.read(cfg_path)

class Config:
    """Base configuration"""

    # os.getenv() takes in the key
    # if the key does not exist, the second parameter will be returned
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev') # for session signing

    # In order to set debug mode reliably, use the --debug option on the 
    # flask or flask run command.
    # Using the option is recommended. While it is possible to set DEBUG 
    # in your config or code, this is strongly discouraged. It can’t be 
    # read early by the flask run command, and some systems or extensions 
    # may have already configured themselves based on a previous value.
    DEBUG = os.getenv('DEBUG', True)
    TESTING = os.getenv('TESTING', True)

class DevelopmentConfig(Config):
    """Development configuration"""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    """Testing configuration"""
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    "Production configuration"
    # the SECRET_KEY will be overriden and taken from the .env file
    # .env files are generally not pushed to version control
    # they are meant to be created and set on the production machines
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

# configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable
from app.mod_auth.auth_controller import mod_auth as auth_module
from app.mod_main.main_controller import mod_main as main_module
from app.mod_exploration.exploration_controller import mod_explore as explore_module
from app.mod_prediction.prediction_controller import mod_prediction as prediction_module
# from app.mod_exploration.controller import mod_exploration as exploration_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(main_module)
app.register_blueprint(explore_module)
app.register_blueprint(prediction_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
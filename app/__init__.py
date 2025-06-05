from flask import Flask
from .routes import main
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')))
    app.secret_key = 'loganalyzer_secret'
    app.register_blueprint(main)
    return app

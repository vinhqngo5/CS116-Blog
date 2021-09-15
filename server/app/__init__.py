
from flask import Flask, jsonify
from . import db
from .routes import api

def create_app(test_config=None):
    app = Flask(__name__)
    
    cursor = db.connect_db()

    app.register_blueprint(api, url_prefix='/api')

    return app
import os

from flask import Flask, jsonify


def create_app(test_config=None):
    app = Flask(__name__)
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/f')
    def ok():
        return jsonify({
            "a": "b"
        })

    return app
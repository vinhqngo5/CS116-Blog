import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    ## DATABASE CONFIG

    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    host = '127.0.0.1'
    database ='blog'

    CONNECTION_STRING = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'

    app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING

    try:
        db.init_app(app)
    except Exception as e:
        print(e)
    
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app
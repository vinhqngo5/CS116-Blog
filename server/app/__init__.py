import os
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    ## JWT CONFIG
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=365)
    jwt.init_app(app)

    ## DATABASE CONFIG

    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    host = '127.0.0.1'
    database ='blog'

    CONNECTION_STRING = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'

    app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING

    try:
        with app.app_context():
            db.init_app(app)
    except Exception as e:
        print(e)
        exit(1)
    
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    return app

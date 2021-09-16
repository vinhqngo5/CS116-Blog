from flask import Blueprint
from .home import home_routes
from .auth import auth_routes
from .post import post_routes

api = Blueprint('api', __name__)

def middleware():
    print('middleware')

api.before_request_funcs = {
    'home': [middleware]
}

api.register_blueprint(home_routes)
api.register_blueprint(auth_routes, url_prefix='/auth')
api.register_blueprint(post_routes, url_prefix='/post')
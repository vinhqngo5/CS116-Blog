from flask import Blueprint, jsonify

post_routes = Blueprint('post', __name__)

@post_routes.route('/')
def index():
    return jsonify('ok'), 201
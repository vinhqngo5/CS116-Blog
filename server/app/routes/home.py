from flask import Blueprint, jsonify

home_routes = Blueprint('home', __name__)

@home_routes.route('/')
def index():
    return jsonify('ok'), 201
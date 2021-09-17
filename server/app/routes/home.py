from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

home_routes = Blueprint('home', __name__)

@home_routes.route('/')
@jwt_required()
def index():
    return jsonify('ok'), 201
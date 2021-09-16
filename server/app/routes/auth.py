from flask import Blueprint, request, jsonify, g
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
import os
import dotenv 
dotenv.load_dotenv()
from app.models.user import User

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        payload = request.get_json()
        token = payload['token']
        
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.environ['CLIENT_ID'])
        except Exception as e:
            print(e)
            return jsonify({'error': 'Invalid token'}), 400
        
        now = datetime.now().isoformat()

        users = User.query.all()
        for user in users:
            print(user.email)
        return jsonify({'payload': 'ok'})
        
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500
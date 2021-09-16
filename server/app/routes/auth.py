from flask import Blueprint, request, jsonify, g
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
from app.db import get_db
import os
import dotenv 
dotenv.load_dotenv()

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

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user WHERE email = %s', (idinfo['email'],))
        data = cursor.fetchall()

        if data:
            # USER LOGIN: update user last login
            cursor.execute('UPDATE user SET lastLogin = %s WHERE email = %s', (now, idinfo['email'],))
            conn.commit()
        else:
            # USER FIRST LOGIN: create new user
            cursor.execute('''
                INSERT INTO user (firstName, lastName, email, registeredAt, lastLogin)
                VALUES (%s, %s, %s, %s, %s)''',
                (idinfo['family_name'], idinfo['given_name'], idinfo['email'], now, now,))
        
        return jsonify({'email': idinfo['email'],
                        'new_user': False if data else True,
                        'jwt': ''}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500
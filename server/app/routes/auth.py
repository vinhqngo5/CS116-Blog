from flask import Blueprint, request, jsonify
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
from flask_jwt_extended import create_access_token

import slugify
import os

from app.models import User
from app import db

import dotenv 
dotenv.load_dotenv()

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        payload = request.get_json()
        token = payload['token']
        
        try:
            info = id_token.verify_oauth2_token(token, requests.Request(), os.environ['CLIENT_ID'])
        except Exception as e:
            print(e)
            return jsonify({'error': 'Invalid token'}), 400
        
        now = datetime.now().isoformat()

        user = User.query.filter_by(email=info['email']).first()

        firstLogin = True

        if user:
            # USER LOGIN:
            user.lastLogin = now
            db.session.commit()
            firstLogin = False
        else:
            # USER FIRST LOGIN:
            username = info['email'].split('@')[0]
            dup_username = User.query.filter(User.slug.ilike(username+'%')).all()

            slugify_unique = slugify.UniqueSlugify(uids=dup_username, to_lower=True)
            slug = slugify_unique(username)
            
            user = User(firstName=info['family_name'], lastName=info['given_name'], email=info['email'],
                        slug=slug, avatarLink=info['picture'], registeredAt=now, lastLogin=now)
            
            print('a')
            db.session.add(user)
            db.session.commit()
        
        jwt = create_access_token(identity=info['email'])

        return jsonify({
            'email': info['email'],
            'slug': slug,
            'firstLogin': firstLogin,
            'jwt': jwt}
        ),201
        
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500
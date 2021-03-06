from flask import Blueprint, request, jsonify
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

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
        slug = ''

        if user:
            # USER LOGIN:
            user.lastLogin = now
            db.session.commit()
            slug = user.slug
            firstLogin = False
        else:
            # USER FIRST LOGIN:
            username = info['email'].split('@')[0]
            users_dup_slug = User.query.filter(User.slug.ilike(username+'%')).all()
            dup_slug = [user.slug for user in users_dup_slug]
            slugify_unique = slugify.UniqueSlugify(uids=dup_slug, to_lower=True)
            slug = slugify_unique(username)
            
            user = User(firstName=info['family_name'], lastName=info['given_name'], email=info['email'],
                        slug=slug, avatarLink=info['picture'], registeredAt=now, lastLogin=now)
            
            print('a')
            db.session.add(user)
            db.session.commit()
        
        accessToken = create_access_token(identity=user.id)
        refreshToken = create_refresh_token(identity=user.id)

        return jsonify({
            'userInfo':
            {
                'email': user.email,
                'slug': user.slug,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'avatarLink': user.avatarLink,
            }, 
            'auth':
            {
                'firstLogin': firstLogin,
                'accessToken': accessToken,
                'refreshToken': refreshToken
            }
            }
        ),201
        
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Something went wrong'}), 500


@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"accessToken":access_token}), 201
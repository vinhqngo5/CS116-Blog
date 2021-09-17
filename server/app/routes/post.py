from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Post, db
from slugify import slugify

from datetime import datetime

post_routes = Blueprint('post', __name__)

@post_routes.route('/create', methods=['POST'])
@jwt_required()
def index():
    userEmail = get_jwt_identity()
    body = request.json
    user = User.query.filter_by(email=userEmail).first()

    now = datetime.now().isoformat()

    ## create slug
    
    slug = slugify(user.slug + body['title'], max_length=50, to_lower=True)

    ## get summary
    summary = ''
    contentSplit = body['content'].split(' ')
    if len(contentSplit) > 40:
        summary = ' '.join(contentSplit[:40])
    else:
        summary = ' '.join(contentSplit)

    post = Post(
        authorId=user.id,
        title=body['title'],
        subtitle=body['subtitle'],
        slug=slug,
        summary=summary,
        published=0 if body['isDraft'] is True else 1,
        createdAt=now,
        bannerLink=body['banner'],
        publishedAt=None if body['isDraft'] else now,
        content=body['content']
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({'test': post.slug}), 201
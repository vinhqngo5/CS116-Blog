from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Post, db
from slugify import UniqueSlugify, slugify

from datetime import datetime

post_routes = Blueprint('post', __name__)

@post_routes.route('/create', methods=['POST'])
@jwt_required()
def create_post():
    try:
        userId = get_jwt_identity()
        body = request.json
        user = User.query.filter_by(id=userId).first()

        now = datetime.now().isoformat()

        ## create slug
        slug = slugify(body['title'], to_lower=True, max_length=40)
        posts_slug = Post.query.filter(Post.slug.ilike(slug+'%')).all()
        dup_slug = [post.slug for post in posts_slug]
        
        unique_slug = UniqueSlugify(uids=dup_slug, to_lower=True, max_length=50)
        slug = unique_slug(body['title'])

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

        return jsonify({'slug': post.slug}), 201
    except Exception as e:
        print(e)
        return jsonify({"msg": "Something went wrong"}), 500


@post_routes.route('/fetch', methods=['POST'])
@jwt_required()
def fetch_post():
    body = request.json 
    userId = get_jwt_identity()
    posts = Post.query.filter_by(authorId=userId, published=1).order_by(Post.publishedAt.desc())
    
    
    post_titles = [post.slug for post in posts]

    return jsonify({
        'payload': post_titles
    }), 201



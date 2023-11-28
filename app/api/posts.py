from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Post, Comment, User, Ingredient
from flask_jwt_extended import *
from datetime import datetime

bp = Blueprint('post', __name__, url_prefix='/posts')


# 레시피 리스트
@bp.route('/', methods=['GET'])
def get_posts():
    page_no = request.args.get('pageNo', type=int, default=1)
    page_size = request.args.get('pageSize', type=int, default=10)

    offset = (page_no - 1) * page_size

    posts = list(db.session
                 .query(Post)
                 .order_by(Post.id.desc())
                 .offset(offset)
                 .limit(page_size)
                 .all())

    resp = {
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "create_date": post.create_date,
                "username": get_username_hook(post.user_id)
            }
            for post in posts
        ],
        "pageNo": page_no,
        "pageSize": page_size
    }

    return jsonify(resp), 200


# 레시피 상세
@bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    comments = db.session.query(Comment).filter_by(post_id=post_id)

    resp = {
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "create_date": post.create_date,
            "modify_date": post.modify_date,
            "price": post.price,
            "like": len(post.liker)
        },
        "comments": [
            {
                "id": comment.id,
                "content": comment.content,
                "user_id": comment.user_id,
                "username": get_username_hook(comment.user_id),
                "create_date": comment.create_date,
                "modify_date": comment.modify_date,
                "like": len(comment.liker)
            }
            for comment in comments
        ]
    }

    return jsonify(resp), 200


# 레시피 삭제
@bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required(optional=True)  # jwt_required에서 optional=True로 변경하여 JWT가 없어도 요청을 처리할 수 있도록 함
def delete_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()

    # 로그인한 경우에만 유저 정보를 가져옴
    current_user = get_jwt_identity() if get_jwt_identity() else None

    # 삭제 권한 확인
    if current_user and post.user_id != current_user['id']:
        return jsonify({
            "result": "failed",
            "message": "삭제 권한이 없음"
        }), 400

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        "result": "success",
        "post_id": post_id,
        "message": "레시피 삭제 성공"
    }), 200


# 레시피 폼 등록
@bp.route('/forms', methods=['POST'])
@jwt_required(optional=True)  # jwt_required에서 optional=True로 변경하여 JWT가 없어도 요청을 처리할 수 있도록 함
def create_post():
    req = request.get_json()

    post = req['post']
    ingredients = req['ingredients']
    
    # 로그인한 경우에만 유저 정보를 가져옴
    current_user = get_jwt_identity() if get_jwt_identity() else None

    price = 0

    if ingredients:
        for ingredient in ingredients:
            price += ingredient['price'] * ingredient['quantity'] / ingredient['unit']

    new_post = Post(title=post['title'], content=post['content'], price=price, create_date=datetime.now(), user_id=current_user['id'])

    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "result": "success",
        "post_id": new_post.id,
        "message": "레시피 등록 성공"
    }), 200

# 이하 생략

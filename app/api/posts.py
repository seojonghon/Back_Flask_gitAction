from flask import Blueprint, request, jsonify
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
@jwt_required()
def delete_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()

    if post.user_id != user.id:
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
@jwt_required()
def create_post():
    req = request.get_json()

    post = req['post']
    ingredients = req['ingredients']
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()
    price = 0

    if ingredients:
        for ingredient in ingredients:
            price += ingredient['price'] * ingredient['quantity'] / ingredient['unit']

    new_post = Post(title=post['title'], content=post['content'], price=price, create_date=datetime.now(), user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "result": "success",
        "post_id": new_post.id,
        "message": "레시피 등록 성공"
    }), 200


# 레시피 재료
@bp.route('/forms/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = db.session.query(Ingredient).all()

    resp = {
        "ingredients": [
            {
                "id": ingredient.id,
                "name": ingredient.name,
                "price": ingredient.price,
                "unit": ingredient.unit
            }
            for ingredient in ingredients
        ]
    }

    return jsonify(resp), 200


# 레시피 수정 폼
@bp.route('/forms/<int:post_id>', methods=['GET'])
@jwt_required()
def get_form(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()

    if post.user_id != user.id:
        return jsonify({
            "result": "failed",
            "message": "수정 권한이 없음"
        })

    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content
    }), 200


# 레시피 수정 폼 등록
@bp.route("/forms/<int:post_id>", methods=['PUT'])
def update_post(post_id):
    req = request.get_json()
    updated_post = req['post']
    ingredients = req['ingredients']
    price = 0

    if ingredients:
        for ingredient in ingredients:
            price += ingredient['price'] * ingredient['quantity'] / ingredient['unit']

    post = Post.query.get(post_id)
    post.title = updated_post['title']
    post.content = updated_post['content']
    post.price = price
    post.modify_date = datetime.now()

    db.session.commit()

    return jsonify({
        "result": "success",
        "message": "레시피 수정 성공"
    }), 200


# 레시피 좋아요
@bp.route('/<int:post_id>/likes', methods=['POST'])
@jwt_required()
def create_like(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()

    if user.id == post.user_id:
        return jsonify({
            "result": "failed",
            "message": "자신이 작성한 레시피 좋아요 불가"
        }), 400

    if user in post.liker:
        return jsonify({
            "result": "failed",
            "message": "중복 좋아요 불가"
        }), 400

    post.liker.append(user)

    db.session.commit()

    return jsonify({
        "result": "success",
        "message": "레시피 좋아요 성공"
    }), 200


# 댓글 작성
@bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    req = request.get_json()
    post = db.session.query(Post).filter_by(id=post_id).first()
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()
    comment = Comment(
        post_id=post_id,
        content=req['content'],
        create_date=datetime.now(),
        user_id=user.id
    )

    post.comment_set.append(comment)

    db.session.commit()

    return jsonify({
        "result": "success",
        "comment_id": comment.id,
        "message": "댓글 작성 성공"
    }), 200


# 댓글 좋아요
@bp.route('/comments/<int:comment_id>/likes', methods=['POST'])
@jwt_required()
def create_comment_like(comment_id):
    comment = db.session.query(Comment).filter_by(id=comment_id).first()
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()

    if user.id == comment.user_id:
        return jsonify({
            "result": "failed",
            "message": "자신이 작성한 댓글 좋아요 불가"
        }), 400

    if user in comment.liker:
        return jsonify({
            "result": "failed",
            "message": "중복 좋아요 불가"
        }), 400

    comment.liker.append(user)

    db.session.commit()

    return jsonify({
        "result": "success",
        "message": "댓글 좋아요 성공"
    }), 200


# 댓글 수정
@bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    req = request.get_json()
    comment = db.session.query(Comment).filter_by(id=comment_id).first()
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()

    if user.id != comment.user_id:
        return jsonify({
            "result": "failed",
            "message": "댓글 수정 권한이 없음"
        }), 400

    comment.content = req['content']
    comment.modify_date = datetime.now()

    db.session.commit()

    return jsonify({
        "result": "success",
        "message": "댓글 수정 성공"
    }), 200


# 댓글 삭제
@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    comment = db.session.query(Comment).filter_by(id=comment_id).first()
    user = db.session.query(User).filter_by(username=get_jwt_identity()).first()

    if user.id != comment.user_id:
        return jsonify({
            "result": "failed",
            "message": "댓글 삭제 권한이 없음"
        }), 400

    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        "result": "success",
        "message": "댓글 삭제 성공"
    }), 200


def get_username_hook(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()

    if user:
        return user.username
    else:
        return 'null'

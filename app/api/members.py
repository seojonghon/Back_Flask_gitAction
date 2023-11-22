from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app import bcrypt, jwt_redis
from flask_jwt_extended import *
from datetime import datetime, timedelta, timezone
from flask_wtf.csrf import generate_csrf


bp = Blueprint('members', __name__, url_prefix='/members')


# 회원가입
@bp.route('/forms', methods=['POST'])
def signup():
    user = request.get_json()

    username = user['username']
    hashed_password = bcrypt.generate_password_hash(user['password']).decode('utf-8')
    email = user['email']

    # 중복 가입 조회
    if User.query.filter_by(username=username).one_or_none():
        return jsonify({
            "result": "failed",
            "message": "중복 가입"
        }), 400

    user = User(username=username, password=hashed_password, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "result": "success",
        "user_id": user.id,
        "message": "회원가입 성공"
    }), 200


# 로그인
@bp.route('/login', methods=['POST'])
def login():
    user = request.get_json()
    username = user['username']
    password = user['password']

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not bcrypt.check_password_hash(pw_hash=user.password, password=password):
        return jsonify({
            "result": "failed",
            "message": "등록되지 않은 아이디거나 비밀번호가 일치하지 않음"
        }), 400

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    resp = jsonify({
        "result": "success",
        "user_id": user.id,
        "username": username,
        "access_token": access_token,
        "csrf_token": generate_csrf_token(),
        "message": "로그인 성공"
    })

    set_access_cookies(response=resp, encoded_access_token=access_token)
    set_refresh_cookies(response=resp, encoded_refresh_token=refresh_token)

    jwt_redis.set(refresh_token, username, ex=timedelta(days=14))

    return resp, 200


# 사용자 삭제
@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    cur_user = db.session.query(User).filter_by(username=get_jwt_identity()).first()

    if user.id != cur_user.id:
        return jsonify({
            "result": "failed",
            "message": "삭제 권한이 없음"
        }), 400

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "result": "success",
        "user_id": user.id,
        "message": "deleted"
    }), 200


# 로그아웃
@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({
        "result": "success",
        "message": "로그아웃 성공"
    })

    jwt_redis.delete(request.cookies.get('refresh_token_cookie'))
    unset_jwt_cookies(resp)

    return resp, 200


# Refresh-Token 발급
@bp.route('/tokens', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    token = jwt_redis.get(request
                          .cookies
                          .get('refresh_token_cookie'))
    username = User.query.filter_by(username=get_jwt_identity()).one_or_none()

    if token is None or username is None:
        return jsonify({
            "result": "failed",
            "message": "refresh failed"
        }), 400

    token = request.cookies.get('refresh_token_cookie')
    username = get_jwt_identity()

    resp = jsonify({
        "result": "success",
        "message": "refresh success"
    })

    access_token = create_access_token(identity=username)
    set_access_cookies(response=resp, encoded_access_token=access_token)

    exp_timestamp = get_jwt()['exp']
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(hours=10))

    if target_timestamp > exp_timestamp:
        jwt_redis.delete(token)

        refresh_token = create_refresh_token(identity=username)
        set_refresh_cookies(response=resp, encoded_refresh_token=refresh_token)

        jwt_redis.set(refresh_token, username, ex=timedelta(days=14))

    return resp, 200


# 아이디 중복 체크
@bp.route('/validation', methods=['POST'])
def validate():
    username = request.get_json()['username']

    if db.session.query(User).filter_by(username=username).first():
        return jsonify({
            "message": "이미 가입된 아이디입니다."
        })
    else:
        return jsonify({
            "message": "사용 가능한 아이디입니다."
        })


def generate_csrf_token():
    return generate_csrf()

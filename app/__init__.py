from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import redis
import os


"""
데이터베이스 객체가 생성될 때 이 네이밍 규칙이 적용됨
테이블, 제약 조건 등을 생성할 때 개발자가 일일이 이름을 정의할 필요가 없어짐
"""

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
jwt_redis = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=6379, db=0, decode_responses=True)


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    """
    Application Factory Pattern     
    """

    # CORS(app, resources={r'*': {'origins': 'http://10.0.0.4'}})
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    """
    DB
    - Development, Staging 환경: SQlite
    - Production 환경: PostgresSQL
    환경에 맞는 DB를 자동으로 플러그
    """
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    """
    Blueprints
    """

    from .api import posts, members

    app.register_blueprint(posts.bp)
    app.register_blueprint(members.bp)

    return app

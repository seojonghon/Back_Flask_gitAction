import os
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SQLALCHEMY_TRACK_MODIFICATIONS = False


JWT_DECODE_ALGORITHMS = ['HS256']
JWT_TOKEN_LOCATION = ['headers']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)
JWT_COOKIE_SECURE = False
JWT_COOKIE_CSRF_PROTECT = True
JWT_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
JWT_CSRF_CHECK_FORM = True
JWT_CSRF_IN_COOKIES = True

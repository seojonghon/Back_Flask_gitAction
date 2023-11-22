from config.default import *
from datetime import timedelta


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'app.db'))

SECRET_KEY = "b'\xa2\xa4A\x84\x9f\x86\x82\x05G\xe2\xb2eD\x18p\x01'"


# JWT secret key
# python -c 'import os; print(os.urandom(16))'
JWT_SECRET_KEY = b'\xb4\xc4\x8b\xfbU\xc1\x8d\x1d\x82\xca\x08^\x0bO\x05I'
# Type of algorithm
JWT_DECODE_ALGORITHMS = ['HS256']
# Location to check when validate JWT token
JWT_TOKEN_LOCATION = ['headers']
# JWT Access token expiration
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
# JWT refresh token expiration
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)
# If not production, off secure
JWT_COOKIE_SECURE = False
# CSRF protection
JWT_COOKIE_CSRF_PROTECT = True
# Check CSRF of method
JWT_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
# Check CSRF of forms
JWT_CSRF_CHECK_FORM = True
# Check CSRF in cookies
JWT_CSRF_IN_COOKIES = True


# REDIS HOST
REDIS_HOST = '0.0.0.0'

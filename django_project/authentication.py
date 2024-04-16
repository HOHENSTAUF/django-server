import jwt
import datetime
from constance import config
from user.models import User


def create_access_token(id):
    user = User.objects.get(id=id)
    return jwt.encode({
        'user_id': id,
        'username': user.username,
        'email': user.email,

        'exp': datetime.datetime.now(datetime.timezone.utc) + config.ACCESS_LIFETIME,
        'iat': datetime.datetime.now(datetime.timezone.utc),
    }, 'access_secret', algorithm='HS256')


def create_refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + config.REFRESH_LIFETIME,
        'iat': datetime.datetime.now(datetime.timezone.utc),
    }, 'refresh_secret', algorithm='HS256')

def decode_access_token(token):
    return jwt.decode(token, 'access_secret', algorithms=['HS256'])


def decode_refresh_token(token):
    return jwt.decode(token, 'refresh_secret', algorithms=['HS256'])

import jwt, datetime
from constance import config

def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.now() + datetime.timedelta(seconds=config.ACCESS_TOKEN_LIFETIME),
        'iat': datetime.datetime.now()
    }, 'refresh_secret', algorithm='HS256')
import jwt
from rest_framework.exceptions import AuthenticationFailed
import os
jwt_secret_key = os.getenv('JWT_SECRET_KEY','e354wfsdfsdffg')


def decode_jwt_token(token):
    try:
        payload= jwt.decode(token,jwt_secret_key,algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Acces token Expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid Acces Token')
    
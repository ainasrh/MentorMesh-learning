import jwt
from datetime import datetime,timedelta
import os
from django.conf import settings
jwt_secret_key = os.getenv('JWT_SECRET_KEY')
algorthm='HS256'

def generate_acces_token(user):
    payload= {
        'user_id':user.id,
        'username':user.username,
        'email':user.email,
        'role':user.role,
        'exp':datetime.utcnow() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        'iat':datetime.utcnow(),
    }

    token=jwt.encode(payload,jwt_secret_key,algorithm=algorthm)
    return token

def generate_refresh_token(user):
    payload = {
        "user_id":user.id,
        "exp":datetime.utcnow() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        "iat":datetime.utcnow(),
    }
    
    return jwt.encode(payload,jwt_secret_key,algorithm=algorthm)
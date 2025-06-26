from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from course.utils.decode_token import decode_jwt_token
import logging

logger = logging.getLogger(__name__)



class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self,request):
        auth_header =request.headers.get("Authorization")
    

        if not auth_header or not auth_header.startswith("Bearer "):
            
            return None
        
        token = auth_header.split(" ")[1]
        try:

            payload=decode_jwt_token(token)
        except AuthenticationFailed as e:
            logger.error(f'Token decode error: {e}')
            raise AuthenticationFailed("Invalid or expired token")
        
        # create a empty object 
        user=type('User',(),{})()
        user.id = payload.get("user_id")
        user.username = payload.get('username')
        user.role=payload.get('role') 

    
        return (user,None)

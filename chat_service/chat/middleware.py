from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from .RabbitmqFiles.get_user_publisher import get_user_info
import logging
from rest_framework_simplejwt.exceptions import TokenError

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        token = parse_qs(query_string).get('token')

        if token:
            try:
                logger.info(f"🔐 Received token: {token[0]}")
                access_token = AccessToken(token[0])  # May raise 
                logger.info("✅ Access token decoded successfully")

                user_id=access_token.get('user_id')
                scope['user']=get_user_info(user_id)
            except TokenError as e:
                logger.error(f"❌ Token error: {str(e)}")
                scope['user'] = AnonymousUser()
            except Exception as e:
                logger.error(f"❌ Unknown error: {str(e)}")
                scope['user'] = AnonymousUser()

        else:
            logger.warning("⚠️ No token found in query string")
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

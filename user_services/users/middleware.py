from django.utils.timezone import now
from django.contrib.auth import get_user_model

import logging

logger=logging.getLogger(__name__)

class UpdateLastLoginMiddleware:
    logger.info(f"Update LOgin Middle ware working")
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response =self.get_response(request)
        
        if request.user.is_authenticated:
            user=request.user
            User=get_user_model()
            User.objects.filter(pk=user.pk).update(last_login=now())

        return response  
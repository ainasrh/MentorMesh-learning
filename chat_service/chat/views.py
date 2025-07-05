from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .RabbitmqFiles.get_user_publisher import get_user_info
from rest_framework.permissions import IsAuthenticated
from.models import ChatRoom
from .Serializers import ChatRoomSerializer

# Create your views here

class CreateRoomApi(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data,context={'request':request})

        
        # sort user id ascendingly
        user1,user2 = sorted(request.user.id,target_user_id)

        # Create or get room 
        room,created = ChatRoom.objects.get_or_create(user1=user1,user2=user2)
        return Response({"room_id":room.Room_id})
        
    
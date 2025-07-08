from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .RabbitmqFiles.get_user_publisher import get_user_info
from rest_framework.permissions import IsAuthenticated
from.models import ChatRoom,Message
from .Serializers import ChatRoomSerializer,MessageSerializer
import logging

logger = logging.getLogger(__name__)


# Create your views here

class CreateRoomApi(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            room = serializer.save()
            return Response(serializer.to_representation(room), status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        


class RoomMessagesView(APIView):
    logger.info("room message working")
    def get(self,request,room):
        logger.info(f'recieved {room}')
        room_instance = ChatRoom.objects.get(room_id=room)
        logger.info(f"getted room id {room_instance}")

        chat_history = Message.objects.filter(room=room_instance.id).order_by('timestamp')
        serializer = MessageSerializer(chat_history,many=True)
        logger.info(f'data {serializer.data}')
        return Response(serializer.data,status=status.HTTP_200_OK)
    
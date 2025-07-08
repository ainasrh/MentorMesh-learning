from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
from asgiref.sync import sync_to_async
from .models import ChatRoom,Message
from .RabbitmqFiles.get_user_publisher import get_user_info
from django.contrib.auth.models import AnonymousUser


logger= logging.getLogger(__name__)
class ChatConsumer(AsyncWebsocketConsumer):
    # This function will work Automaticaly when Websocket Connect

    async def connect(self):
           
          print("websocket connected Succesfully")
        #   Take the room_name from Websocket URL
          self.room_name = self.scope['url_route']['kwargs']['room_name']
          self.room_group_name=f"chat_{self.room_name}"
          
        #   Join the group equal to Room name                     self.channel_name it will create unique id automatic for every websocket connect
          await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        #   Accept the Websocket connection
          await self.accept()
    # It will Automaticaly work when disconnect websocket
    async def disconnect(self,close_code):
      print("websocket disconnected")
        #   Leave the group
      await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
    
    async def receive(self, text_data):
          data=json.loads(text_data)
        #  Get message from python dict
          message = data['message']
        # "self.Scope" its take request object like request in django views 
        # here take requested username
          user = self.scope['user']

          user = self.scope.get('user')

          username=user.get('username')
          user_id=user.get('id')


          # user_details=get_user_info(user_id)

          logger.info(f'scope user {username}')


          await self.save_message(self.room_name,user_id,message)


        # send the messge to everyone inside the room Group
          await self.channel_layer.group_send(
                # define which group want to send
              self.room_group_name ,
              {     
                   #call type function
                    'type':'chat_message',
                    'message': message,
                    'sender':user_id,
              }
        )

    async def chat_message(self,event):
         await self.send(text_data=json.dumps({"message":event['message'],"sender":event['sender']}))



    @sync_to_async
    def save_message(self, room_id, user_id, message):
      
        try:
            user = user_id
            room = ChatRoom.objects.get(room_id=room_id)
            Message.objects.create(room=room, sender=user, content=message)
        except Exception as e:
            print("Error saving message:", e)


                 
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger= logging.Logger(__name__)
class ChatConsumer(AsyncWebsocketConsumer):
    # This function will work Automaticaly when Websocket Connect

    async def connect(self):
          print("websocker connected Succesfully")
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
      await self.channel_layer.group_discart(self.room_group_name,self.channel_name)
    
    async def receive(self, text_data):
        #  Change to json into python dict
          data=json.loads(text_data)
        #  Get message from python dict
          message = data['message']
        # "self.Scope" its take request object like request in django views 
        # here take requested username
          user= self.scope['user'].username

        # send the messge to everyone inside the room Group
          await self.channel_layer.group_send(
                # define which group want to send
              self.room_group_name ,
              {     
                   #check available any function same as type (chat_message) and call that
                    'type':'chat_message',
                    'message': f'{user}: {message}'
              }
        )

    async def chat_message(self,event):
         await self.send(text_data=json.dumps({"message":event['message']}))






                 
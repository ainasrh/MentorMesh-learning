from django.db import models
import uuid

class ChatRoom(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 
    user1 = models.IntegerField()
    user2 = models.IntegerField()

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Room Between User {self.user1} and User {self.user2}"
    

class Message(models.Model):
    room  = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='messages')
    sender = models.IntegerField()
    content = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in room {self.room.room_id} "

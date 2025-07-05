from django.db import models
import uuid

# Create your models here.


class ChatRoom(models.Model):
    Room_id = models.UUIDField(default=uuid.uuid4, unique=True,editable=False)
    user1 = models.IntegerField()
    user2 = models.IntegerField()

    class Meta:
        unique_together = ('user1', 'user2')
    
    def __str__(self):
        return f"Room Between User {self.user1} and User {self.user2}"
    
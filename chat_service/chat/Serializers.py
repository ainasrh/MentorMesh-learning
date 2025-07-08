from rest_framework import serializers
from .models import ChatRoom,Message
from .RabbitmqFiles.get_user_publisher import get_user_info

class ChatRoomSerializer(serializers.Serializer):
    target_user_id = serializers.IntegerField()
    room_id = serializers.UUIDField(read_only=True)

    def validate(self, data):
        target_user_id = data.get('target_user_id')
        if target_user_id is None:
            raise serializers.ValidationError({"error": "target_user_id is required"})

        try:
            get_user_info(target_user_id)
        except:
            raise serializers.ValidationError({"error": "User not found"})

        return data

    def save(self, **kwargs):
        target_user_id = self.validated_data['target_user_id']
        request_user_id = self.context['request'].user.id

        user1, user2 = sorted([target_user_id, request_user_id])
        room, _ = ChatRoom.objects.get_or_create(user1=user1, user2=user2)
        return room

    def to_representation(self, instance):
        return {
            "room_id": instance.room_id  
        }

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']
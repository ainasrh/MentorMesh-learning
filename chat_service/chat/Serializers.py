from rest_framework import serializers
from RabbitmqFiles.get_user_publisher import get_user_info
from rest_framework import status

class ChatRoomSerializer(serializers.Serializer):
    target_user_id = serializers.IntegerField()

    def validate(self,validation_data):
        target_user_id = validation_data.get('target_user_id')

        if target_user_id is None:
            raise serializers.ValidationError({"error":"target_user_id is required "},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            target_user = get_user_info(target_user_id)
        except:
            raise serializers.ValidationError({"error":"user is not found in this target user id"},status=status.HTTP_404_NOT_FOUND) 
    
        return validation_data
    

    def save(self,validated_data):
        target_user_id = validated_data.get('target_user_id')
        request_user_id = self.context.get('request').user.id
        
        

           
        


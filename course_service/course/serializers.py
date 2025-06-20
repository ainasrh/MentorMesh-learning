from rest_framework import serializers
from .models import *
from course.rabbitmq_publisher import get_user_info
import logging

logger=logging.getLogger(__name__)

    
class CourseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseVideo
        fields='__all__'


    def validate(self,validation_data):
        user =self.context.get('request').user

        course =validation_data.get('course')

        if course.trainer !=user:
            raise serializers.ValidationError({"permission_error":'you can only create video for your courses'})
        

class courseSerializer(serializers.ModelSerializer):
    videos = CourseVideoSerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    thumbnail = serializers.ImageField(write_only=True)
    trainer_info = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'thumbnail_url', 'price', 'thumbnail', 'trainer','is_trending',"videos","trainer_info"]
        read_only_fields = ['trainer']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None

    def validate(self, data):
        user = self.context.get('request').user
        user_data = get_user_info(user.id)

        if "error" in user_data:
            raise serializers.ValidationError("Failed to verify user from user service (via RabbitMQ)")
        if user_data.get("role") != "trainer":
            raise serializers.ValidationError("Only Trainers Can Create or Update courses")

        return data
    
    def get_trainer_info(self,obj):
        from course.rabbitmq_publisher import get_user_info

        try:
            trainer_data=get_user_info(obj.trainer)
            logger.info(f"trainer details {trainer_data}")
        

            if "error" in trainer_data:
                raise serializers.ValidationError("error in rabbitmq")
            return trainer_data
        except Exception as e:
            print(f"Error Fecthing trainer data: {e}")
            return None
        
    # def get_trainer_info(self,obj):
    #     from course.trainer_publisher import trainer_details

    #     try:
    #         trainer_data=trainer_details(obj.trainer)
    #         logger.info(f"trainer details {trainer_data}")
        

    #         if "error" in trainer_data:
    #             raise serializers.ValidationError("error in rabbitmq")
    #         return trainer_data
    #     except Exception as e:
    #         print(f"Error Fecthing trainer data: {e}")
    #         return None

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        print("Incoming is_trending:", self.validated_data.get('is_trending'))
        print("Final count of trending courses:", Course.objects.filter(is_trending=True, is_published=True).count())

        # Get the updated value from validated_data
        is_trending_updated = self.validated_data.get('is_trending', instance.is_trending)

        if is_trending_updated:
            trending_courses = Course.objects.filter(is_trending=True, is_published=True).exclude(id=instance.id).order_by("created_at")
            if trending_courses.count() >= 3:
                oldest = trending_courses.first()
                oldest.is_trending = False
                oldest.save()

        return instance

    def create(self, validated_data):
        validated_data['trainer'] = self.context.get('request').user.id
        return super().create(validated_data)



class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['enrolled_at']


class EnrollmentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model=EnrollmentPartProgress
        fields = '__all__'
        read_only_fields = ['last_watched_at']
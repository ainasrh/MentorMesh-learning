from rest_framework import serializers
from .models import *

    
class CourseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseVideo
        fields='__all__'
        

class courseSerializer(serializers.ModelSerializer):
    videos= CourseVideoSerializer(many=True,read_only=True)
    class Meta:
        model=Course
        fields= "__all__"
        read_only_fields =['trainer'] 

    
    def create(self,validated_data):
        validated_data['trainer'] = self.context['request'].user.id
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
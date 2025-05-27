from rest_framework import serializers
from .models import *

class courseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Course
        fields= "__all__"
        read_only_fields=['trainer']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

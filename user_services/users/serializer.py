from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken 
from django.contrib.auth import get_user_model
import logging

logger=logging.getLogger(__name__)




class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Use create_user to hash password
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    password=serializers.CharField(write_only=True)
    email=serializers.EmailField(write_only=True)

    def validate(self,data):
        email=data.get("email")
        password=data.get("password")
        
        user=authenticate(email=email,password=password)
        print(user)


        #  check is user available with this email and password 

        if not user:
            raise serializers.ValidationError({"error":'invalid username or password'})
        
        # Check email is verified 

        if not user.is_email_verified:
            raise serializers.ValidationError({'error':"Email is not verified"})
        

        refresh_token=RefreshToken.for_user(user)
        access_token=str(refresh_token.access_token)


        return (
        {
            'message':"login succesful",
            "user":{
                "user_id":user.id,
                "username":user.username,
                "email":user.email,
                'is_staff':user.is_staff
            },
            "refresh_token":str(refresh_token),
            "access_token":access_token

        }
        )

        

        # 
        

# FORGOT PASSWORD 

# otp send

class otpRequestSerializer(serializers.Serializer):
    email=serializers.EmailField()


# reset password with otp


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        otp = data.get('otp')
        new_password = data.get('new_password')

        logger.info(f"Serializer received OTP: {otp}")

        try:
            otp_instance = PasswordResetOTP.objects.get(otp_code=otp)
        except PasswordResetOTP.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid OTP'})

        if otp_instance.is_used:
            raise serializers.ValidationError({'error': 'OTP already used'})

        if otp_instance.is_expired():
            raise serializers.ValidationError({'error': "OTP expired"})

        # Set new password
        user = otp_instance.user
        user.set_password(new_password)
        user.save()

        # Mark OTP as used
        otp_instance.is_used = True
        otp_instance.save()

        return data

# change password with old password

class chnagePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=150)
    new_password =serializers.CharField(max_length=150)


    def validate(self,validation_data):
        old_password=validation_data['old_password']
        user=self.context['request'].user
        print('user',user)

        if not user.check_password(old_password):
            raise serializers.ValidationError({'error':'old password is incorrect'})
        
        return validation_data
    
    def save(self):
        user=self.context['request'].user
        new_password=self.validated_data['new_password']

        user.set_password(new_password)
        user.save()
        
        return user
        


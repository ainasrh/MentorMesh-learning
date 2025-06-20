from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .email_utils import send_verification_email,send_otp_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from random import randint
from rest_framework.permissions import IsAuthenticated

import logging
# Create your views here.

logger=logging.getLogger(__name__)

class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            user=serializer.instance
            print('user ',user)

            # sending email verififcation 

            send_verification_email(user,request)



            return Response({"message": "Register Complete Check Your Email For Verification Link"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginAPi(APIView):
    def post(self,request):
        serialized=LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        return Response(serialized.validated_data,status=status.HTTP_200_OK)
    

class LogoutApi(APIView):

    def post(self,request):
        try:

            refresh_token = request.data["refresh_token"]
            token =RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "logout succesfull"},status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({'errror':"invalid or expired refresh token"},status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'erorr':"refresh token required"},status=status.HTTP_400_BAD_REQUEST)
        
# FORGOT PASSWORD 

# SEND OTP TO EMAIL

class RequestOtpAPI(APIView):
    logger.debug("debug is working")
    def post(self,request):
        logger.debug("debug is working")
        logger.info(request.data)
        serialized=otpRequestSerializer(data=request.data)
        if serialized.is_valid():
            email=serialized.validated_data['email']

            try:
                user=User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error":"User with this Email does not exist."},status=status.HTTP_404_NOT_FOUND)
            
            otp=str(randint(100000,999999))
            PasswordResetOTP.objects.create(user=user,otp_code=otp)

            # passing otp to email

            send_otp_email(user,otp)

            return Response({"message":'OTP send to your Email '},status=status.HTTP_200_OK)
        return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)


# CHANGE PASSWORD WITH OTP




class ResetPasswordApi(APIView):
    def post(self, request):
        logger.info(f"Received data: {request.data}")
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        logger.error(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# change password with previous password


class ChangePasswordAPI(APIView):
    permission_classe=[IsAuthenticated]

    def post(self,request):
        serialized=chnagePasswordSerializer(data=request.data,context={'request':request})

        if serialized.is_valid():
            serialized.save()
            return Response({'message':'passwoed changed succesfully'},status=status.HTTP_200_OK)
        return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
        
# Fetch users 
class ALLUsersAPI(APIView):
    def get(self,request):
        try:

            users=User.objects.all()
            serialized=UserSerializer(users,many=True)
            return Response(serialized.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error':'product not found'},status=status.HTTP_404_NOT_FOUND)
        

# get logged user data
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"user {request.user}")
        user_id = request.user.id
        user_details = User.objects.get(id=user_id)
        serializer = UserSerializer(user_details,context={"request":request})
        return Response(serializer.data)
    

class UpdateLoggedUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
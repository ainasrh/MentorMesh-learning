from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User=get_user_model()


#  VERIFICATION EMAIL 
def send_verification_email(user,request):
    print('verification link ',user.email) 

    token = default_token_generator.make_token(user)
    uid=urlsafe_base64_encode(force_bytes(user.pk))

    verification_link=request.build_absolute_uri(
        reverse('verify_email',kwargs={"uidb64":uid,"token":token})
    )

    subject='Verify Your Email'
    message=f'Click the link below to verify your email: \n\n {verification_link}'
    send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email])



#  its set for urls when clicking url it will work this function will work
def verify_email(request,uidb64,token):


    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=get_object_or_404(User,pk=uid)
    except (TypeError,ValueError,OverflowError):
        return HttpResponse('invalid token !')
    

    if default_token_generator.check_token(user,token):
        user.is_email_verified=True
        user.save()
        return HttpResponse('Email Verified succesfully')
    else:
        return HttpResponse('invalid or expired verification')
    



#  ## FOROT  EMAIL OTP

def send_otp_email(email,otp):
    subject='Your Password Reset OTP'
    message =f'Use this otp to Reset your password {otp}. it Expires in 3 minutes' 
    send_mail(subject,message,settings.EMAIL_HOST_USER,[email])

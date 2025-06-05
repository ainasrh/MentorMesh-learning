from django.urls import path
from .views import *
from .email_utils import verify_email

urlpatterns = [
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('register/',RegisterApi.as_view()),
    path('login/',LoginAPi.as_view()),
    path('logout/',LogoutApi.as_view(),name="LoginAPi"),
    path('request-otp/',RequestOtpAPI.as_view(),name='request_otp'),
    path('reset-password/',ResetPasswordApi.as_view(),name='reset-password'),
    path('change-password',ChangePasswordAPI.as_view(),name='change-password'),
    path('users/',ALLUsersAPI.as_view(),name='all-users')

    
    

]
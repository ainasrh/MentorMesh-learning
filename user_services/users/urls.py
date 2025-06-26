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
    path('users/',ALLUsersAPI.as_view(),name='all-users'),
    path('change-password/',ChangePasswordAPI.as_view(),name='change-password'),
    path('users/me/', MeAPIView.as_view(), name='user-me'),
    path('users/update/me/',UpdateLoggedUserAPI.as_view(),name='update-logged-user'),
    path('trainerprofile/create/',CreateTrainerProfile.as_view(),name='join-as-trainer'),
    path('gettrainerprofile/',GetTrainerProfile.as_view(),name='get-trainer-profile'),
    path('trainer/dashboard/',TrainerDashboardAPI.as_view(),name='trainer-dashboard'),
    path('update-user/',UpdateUserAPI.as_view(),name='trainer-dashboard'),
    
    # admin url
    
    path('admin-dashboard/',AdminDashboardAPI.as_view(),name='admin-dashboard'),


]
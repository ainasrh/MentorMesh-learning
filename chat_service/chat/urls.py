from django.urls import path 
from .views import *
urlpatterns = [
    path('create-room/',CreateRoomApi.as_view(),name='create-room'),
    
]
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User

class TestUserRegisterIntegration(APITestCase):
    def setUp(self):
        self.url=reverse('register')

    def test_user_registration_success(self):
        data= {
            "username":"testuser",
            "email":"test@gmail.com",
            "password":"testpassword",
            "role":"trainer",
        }

        response = self.client.post(self.url,data,format='json')
        
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        created_user=User.objects.filter(email='test@gmail.com').first()

        self.assertEqual(created_user.username,"testuser")
        self.assertEqual(created_user.email,"test@gmail.com")



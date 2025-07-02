from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from users.models import User

class UserModelTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="learner1",
            email="learner@gmail.com",
            password='scure',
            role='learner'
        )

        self.trainer = User.objects.create_user(
            username="trainer1",
            email="trainer@gmail.com",
            password="secure",
            role="trainer"

        )

    def test_user_role_is_learner_by_default(self):
        user = User.objects.create_user(
            username="defaultuser",
            email='default@example.com',
            password='pass123'
        )
        self.assertEqual(user.role,"learner")

    def test_is_trainer(self):
        self.assertEqual(self.trainer.role,"trainer")


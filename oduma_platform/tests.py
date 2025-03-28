from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")

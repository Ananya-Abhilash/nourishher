from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def test_register(self):
        response = self.client.post("/api/auth/register/", {"email": "ada@example.com", "password": "StrongPass!123", "first_name": "Ada", "last_name": "Lovelace"})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="ada@example.com").exists())
        self.assertIn("token", response.data)

    def test_login(self):
        User.objects.create_user("ada@example.com", "ada@example.com", "StrongPass!123")
        response = self.client.post("/api/auth/login/", {"email": "ada@example.com", "password": "StrongPass!123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

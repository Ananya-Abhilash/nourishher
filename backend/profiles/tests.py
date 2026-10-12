from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ada@example.com", "ada@example.com", "StrongPass!123")
        self.token = Token.objects.create(user=self.user)
    def test_profile_requires_authentication(self):
        self.assertEqual(self.client.get("/api/profile/").status_code, 401)
    def test_profile_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.put("/api/profile/", {"date_of_birth": "1990-01-01", "biological_sex": "female", "is_pregnant": False}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["biological_sex"], "female")

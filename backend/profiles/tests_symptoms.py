from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Symptom


class SymptomTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("one@example.com", password="StrongPass!123")
        self.other = User.objects.create_user("two@example.com", password="StrongPass!123")
        self.token = Token.objects.create(user=self.user)
        self.payload = {"name": "Fatigue", "severity": 3, "frequency": "daily", "notes": "Afternoons"}

    def auth(self): self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
    def test_create_and_privacy(self):
        self.auth(); response = self.client.post("/api/symptoms/", self.payload, format="json")
        self.assertEqual(response.status_code, 201); self.assertEqual(Symptom.objects.count(), 1)
        Symptom.objects.create(user=self.other, **self.payload)
        self.assertEqual(len(self.client.get("/api/symptoms/").data), 1)
    def test_validation_and_ownership(self):
        self.auth(); self.assertEqual(self.client.post("/api/symptoms/", {**self.payload, "severity": 6}, format="json").status_code, 400)
        self.assertEqual(self.client.post("/api/symptoms/", {**self.payload, "frequency": "always"}, format="json").status_code, 400)
        other = Symptom.objects.create(user=self.other, **self.payload)
        self.assertEqual(self.client.patch(f"/api/symptoms/{other.id}/", {"severity": 4}, format="json").status_code, 404)
    def test_unauthenticated_denied(self): self.assertEqual(self.client.get("/api/symptoms/").status_code, 401)

from datetime import date, timedelta

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import LabReport, LabResult


class LabReportApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner@example.com", "owner@example.com", "StrongPass!123")
        self.other_user = User.objects.create_user("other@example.com", "other@example.com", "StrongPass!123")
        self.token = Token.objects.create(user=self.user)
        self.payload = {
            "test_date": "2026-10-10",
            "results": [
                {"biomarker": "Ferritin", "value": "25.5", "unit": "ng/mL", "reference_low": "15", "reference_high": "150"},
                {"biomarker": "Vitamin B12", "value": "320", "unit": "pg/mL", "reference_low": None, "reference_high": None},
            ],
        }

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_authenticated_user_can_create_report_with_multiple_results(self):
        self.authenticate()
        response = self.client.post("/api/labs/", self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["result_count"], 2)
        self.assertEqual(LabReport.objects.filter(user=self.user).count(), 1)
        self.assertEqual(LabResult.objects.filter(lab_report_id=response.data["id"]).count(), 2)

    def test_unauthenticated_user_cannot_create_or_list_reports(self):
        self.assertEqual(self.client.get("/api/labs/").status_code, 401)
        self.assertEqual(self.client.post("/api/labs/", self.payload, format="json").status_code, 401)

    def test_users_only_see_their_own_reports(self):
        LabReport.objects.create(user=self.other_user, test_date=date.today())
        self.authenticate()
        response = self.client.get("/api/labs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_user_cannot_retrieve_another_users_report(self):
        report = LabReport.objects.create(user=self.other_user, test_date=date.today())
        self.authenticate()
        self.assertEqual(self.client.get(f"/api/labs/{report.id}/").status_code, 404)

    def test_empty_results_are_rejected_without_creating_report(self):
        self.authenticate()
        response = self.client.post("/api/labs/", {"test_date": "2026-10-10", "results": []}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LabReport.objects.count(), 0)

    def test_invalid_numeric_values_are_rejected_without_partial_report(self):
        self.authenticate()
        payload = {"test_date": "2026-10-10", "results": [{"biomarker": "Iron", "value": "not-a-number", "unit": "µg/dL"}]}
        response = self.client.post("/api/labs/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LabReport.objects.count(), 0)

    def test_invalid_reference_ranges_are_rejected_without_partial_report(self):
        self.authenticate()
        payload = {"test_date": "2026-10-10", "results": [{"biomarker": "Iron", "value": "80", "unit": "µg/dL", "reference_low": "100", "reference_high": "50"}]}
        response = self.client.post("/api/labs/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LabReport.objects.count(), 0)

    def test_future_test_dates_are_rejected(self):
        self.authenticate()
        payload = {**self.payload, "test_date": str(date.today() + timedelta(days=1))}
        response = self.client.post("/api/labs/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LabReport.objects.count(), 0)

    def test_report_detail_returns_associated_results(self):
        self.authenticate()
        created = self.client.post("/api/labs/", self.payload, format="json")
        response = self.client.get(f"/api/labs/{created.data['id']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["biomarker"], "Ferritin")

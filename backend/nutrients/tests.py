from datetime import date
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from labs.models import LabReport, LabResult

class AssessmentTests(APITestCase):
    def setUp(self): self.user = User.objects.create_user("a@example.com", password="StrongPass!123"); self.token = Token.objects.create(user=self.user)
    def auth(self): self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
    def test_missing_data_is_insufficient_and_private(self):
        self.auth(); response = self.client.get("/api/nutrients/assessment/")
        self.assertEqual(response.status_code, 200); self.assertTrue(all(item["status"] == "insufficient_data" for item in response.data["results"]))
    def test_outside_recorded_range_flagged(self):
        report = LabReport.objects.create(user=self.user, test_date=date.today())
        LabResult.objects.create(lab_report=report, biomarker="Ferritin", value="12", unit="ng/mL", reference_low="15", reference_high="150")
        self.auth(); result = next(item for item in self.client.get("/api/nutrients/assessment/").data["results"] if item["nutrient"] == "Iron")
        self.assertEqual(result["status"], "potential_concern"); self.assertEqual(result["evidence"][0]["comparison"], "below_recorded_reference_range")
    def test_missing_ranges_do_not_flag(self):
        report = LabReport.objects.create(user=self.user, test_date=date.today())
        LabResult.objects.create(lab_report=report, biomarker="Ferritin", value="1", unit="ng/mL")
        self.auth(); result = next(item for item in self.client.get("/api/nutrients/assessment/").data["results"] if item["nutrient"] == "Iron")
        self.assertEqual(result["status"], "insufficient_data")

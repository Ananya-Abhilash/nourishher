from django.conf import settings
from django.db import models

class LabReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lab_reports")
    test_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class LabResult(models.Model):
    lab_report = models.ForeignKey(LabReport, on_delete=models.CASCADE, related_name="results")
    biomarker = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=64)
    reference_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

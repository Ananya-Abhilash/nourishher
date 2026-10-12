from rest_framework import serializers
from .models import LabReport, LabResult

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = ("id", "biomarker", "value", "unit", "reference_low", "reference_high", "created_at")
        read_only_fields = ("id", "created_at")

class LabReportSerializer(serializers.ModelSerializer):
    results = LabResultSerializer(many=True, read_only=True)
    class Meta:
        model = LabReport
        fields = ("id", "test_date", "created_at", "results")
        read_only_fields = ("id", "created_at", "results")

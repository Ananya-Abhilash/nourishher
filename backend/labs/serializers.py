from datetime import date
from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from .models import LabReport, LabResult


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = ("id", "biomarker", "value", "unit", "reference_low", "reference_high", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_biomarker(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Enter a biomarker name.")
        return value

    def validate_unit(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Enter the unit shown on the lab report.")
        return value

    def validate(self, attrs):
        for field in ("value", "reference_low", "reference_high"):
            value = attrs.get(field)
            if value is not None and not isinstance(value, Decimal):
                raise serializers.ValidationError({field: "Enter a valid numeric value."})
            if value is not None and not value.is_finite():
                raise serializers.ValidationError({field: "Enter a finite numeric value."})
        low, high = attrs.get("reference_low"), attrs.get("reference_high")
        if low is not None and high is not None and low > high:
            raise serializers.ValidationError({"reference_high": "The upper limit must be greater than or equal to the lower limit."})
        return attrs


class LabReportSerializer(serializers.ModelSerializer):
    results = LabResultSerializer(many=True)
    result_count = serializers.SerializerMethodField(read_only=True)
    result_summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LabReport
        fields = ("id", "test_date", "created_at", "results", "result_count", "result_summary")
        read_only_fields = ("id", "created_at", "result_count", "result_summary")

    def validate_test_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Test date cannot be in the future.")
        return value

    def validate_results(self, value):
        if not value:
            raise serializers.ValidationError("Add at least one result to this report.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        results = validated_data.pop("results")
        report = LabReport.objects.create(user=self.context["request"].user, **validated_data)
        LabResult.objects.bulk_create([LabResult(lab_report=report, **result) for result in results])
        return report

    def get_result_count(self, obj):
        return len(obj.results.all())

    def get_result_summary(self, obj):
        names = [result.biomarker for result in obj.results.all()]
        return ", ".join(names[:3]) + (f" +{len(names) - 3} more" if len(names) > 3 else "")

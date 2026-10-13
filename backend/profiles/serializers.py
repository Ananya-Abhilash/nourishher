from rest_framework import serializers
from .models import HealthProfile, Symptom

class HealthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfile
        fields = ("date_of_birth", "biological_sex", "is_pregnant", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ("id", "name", "severity", "frequency", "start_date", "notes", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Enter a symptom name.")
        return value.strip()

    def validate_severity(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Severity must be between 1 and 5.")
        return value

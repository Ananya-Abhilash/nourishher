from rest_framework import serializers
from .models import HealthProfile

class HealthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfile
        fields = ("date_of_birth", "biological_sex", "is_pregnant", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

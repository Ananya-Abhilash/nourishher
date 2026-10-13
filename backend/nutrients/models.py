from django.conf import settings
from django.db import models

class Nutrient(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    food_sources = models.TextField(blank=True)
    pregnancy_notes = models.TextField(blank=True)
    upper_limit = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.name


class NutrientStatus(models.Model):
    class Status(models.TextChoices):
        POTENTIAL_CONCERN = "potential_concern", "Potential concern"
        NO_FLAG = "no_flag_from_available_data", "No flag from available data"
        INSUFFICIENT_DATA = "insufficient_data", "Insufficient data"
        PROFESSIONAL_REVIEW = "needs_professional_review", "Needs professional review"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="nutrient_statuses")
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, related_name="statuses")
    status = models.CharField(max_length=40, choices=Status.choices)
    evidence = models.JSONField(default=list)
    limitations = models.JSONField(default=list)
    assessed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "nutrient"), name="unique_current_nutrient_status")]

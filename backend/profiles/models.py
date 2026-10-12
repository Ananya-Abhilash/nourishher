from django.conf import settings
from django.db import models

class HealthProfile(models.Model):
    class BiologicalSex(models.TextChoices):
        FEMALE = "female", "Female"
        MALE = "male", "Male"
        OTHER = "other", "Other / prefer not to say"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="health_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    biological_sex = models.CharField(max_length=12, choices=BiologicalSex.choices, blank=True)
    is_pregnant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

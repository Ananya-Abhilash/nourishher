from django.db import models

class Nutrient(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    food_sources = models.TextField(blank=True)
    pregnancy_notes = models.TextField(blank=True)
    upper_limit = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.name

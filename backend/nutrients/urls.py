from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import NutrientViewSet, assessment
router = DefaultRouter()
router.register("", NutrientViewSet, basename="nutrient")
urlpatterns = [path("assessment/", assessment, name="nutrient-assessment")] + router.urls

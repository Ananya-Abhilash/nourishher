from rest_framework.routers import DefaultRouter
from .views import NutrientViewSet
router = DefaultRouter()
router.register("", NutrientViewSet, basename="nutrient")
urlpatterns = router.urls

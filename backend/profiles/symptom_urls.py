from rest_framework.routers import DefaultRouter
from .views import SymptomViewSet

router = DefaultRouter()
router.register("", SymptomViewSet, basename="symptom")
urlpatterns = router.urls

from rest_framework import viewsets
from .models import Nutrient
from .serializers import NutrientSerializer
class NutrientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Nutrient.objects.all().order_by("name")
    serializer_class = NutrientSerializer

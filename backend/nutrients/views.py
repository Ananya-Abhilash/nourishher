from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Nutrient
from .serializers import NutrientSerializer
from .services import assess_user_nutrients
class NutrientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Nutrient.objects.all().order_by("name")
    serializer_class = NutrientSerializer


@api_view(["GET"])
def assessment(request):
    return Response(assess_user_nutrients(request.user))

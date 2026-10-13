from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HealthProfile, Symptom
from .serializers import HealthProfileSerializer, SymptomSerializer

class ProfileView(APIView):
    def get(self, request):
        profile, _ = HealthProfile.objects.get_or_create(user=request.user)
        return Response(HealthProfileSerializer(profile).data)
    def put(self, request):
        profile, _ = HealthProfile.objects.get_or_create(user=request.user)
        serializer = HealthProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SymptomViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomSerializer
    http_method_names = ("get", "post", "put", "patch", "delete", "head", "options")

    def get_queryset(self):
        return Symptom.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

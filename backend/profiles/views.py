from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HealthProfile
from .serializers import HealthProfileSerializer

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

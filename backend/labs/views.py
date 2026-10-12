from rest_framework import viewsets
from .models import LabReport
from .serializers import LabReportSerializer

class LabReportViewSet(viewsets.ModelViewSet):
    serializer_class = LabReportSerializer
    def get_queryset(self):
        return LabReport.objects.filter(user=self.request.user).prefetch_related("results")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

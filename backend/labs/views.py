from rest_framework import mixins, viewsets
from .models import LabReport
from .serializers import LabReportSerializer

class LabReportViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = LabReportSerializer

    def get_queryset(self):
        return LabReport.objects.filter(user=self.request.user).prefetch_related("results").order_by("-test_date", "-created_at")

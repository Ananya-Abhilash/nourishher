from django.urls import path
from .views import LabReportViewSet

report_list = LabReportViewSet.as_view({"get": "list", "post": "create"})
report_detail = LabReportViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", report_list, name="lab-report-list"),
    path("<int:pk>/", report_detail, name="lab-report-detail"),
    # Preserve the original Day 1 collection route during the transition.
    path("reports/", report_list, name="lab-report-list-legacy"),
]

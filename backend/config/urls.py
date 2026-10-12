from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/profile/", include("profiles.urls")),
    path("api/labs/", include("labs.urls")),
    path("api/nutrients/", include("nutrients.urls")),
]

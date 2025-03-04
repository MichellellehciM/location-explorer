from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("places.urls")),
    path("api/", include("weather.urls")),  

]

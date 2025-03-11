from django.contrib import admin
from django.urls import path, include
from place.views import home

urlpatterns = [
    path("", home, name="home"),

    path("admin/", admin.site.urls),
    path("api/", include("place.urls")),

]

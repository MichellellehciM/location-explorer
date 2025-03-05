from django.urls import path
from .views import get_location

urlpatterns = [
    path("search/", get_location, name="search"),
]

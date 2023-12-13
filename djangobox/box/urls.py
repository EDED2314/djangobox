from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("locations/", views.Locations.as_view(), name="locations"),
    path("locations/<int:pk>/", views.Location.as_view(), name="location-detail"),
]

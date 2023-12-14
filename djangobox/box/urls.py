from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("locations/", views.LocationListView.as_view(), name="locations"),
    path("locations/<int:pk>/", views.LocationView.as_view(), name="location-detail"),
    path("boxes/", views.LocationListView.as_view(), name="boxes"),
    path("boxes/<int:pk>/", views.LocationView.as_view(), name="box-detail"),
]

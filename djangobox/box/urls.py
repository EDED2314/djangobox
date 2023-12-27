from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inv/locations/", views.LocationListView.as_view(), name="locations"),
    path(
        "inv/locations/<int:pk>/", views.LocationView.as_view(), name="location-detail"
    ),
    path("inv/boxes/", views.BoxListView.as_view(), name="boxes"),
    path("inv/boxes/<int:pk>/", views.BoxView.as_view(), name="box-detail"),
    path("inv/items/", views.ItemListView.as_view(), name="items"),
    path("inv/items/<int:pk>/", views.ItemView.as_view(), name="item-detail"),
    path("inv/items/", views.LoanListView.as_view(), name="loans"),
    path("inv/items/<int:pk>/", views.LoanView.as_view(), name="loan-detail"),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/auth-signin/", views.AuthSignin.as_view(), name="signin"),
    path("accounts/logout/", views.user_logout_view, name="logout"),
]

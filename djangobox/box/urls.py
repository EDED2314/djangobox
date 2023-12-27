from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inv/locations/", views.LocationListView.as_view(), name="locations"),
    path("inv/boxes/", views.BoxListView.as_view(), name="boxes"),
    path("inv/boxes/<int:pk>/", views.BoxView.as_view(), name="box-detail"),
    path("inv/items/", views.ItemListView.as_view(), name="items"),
    path("inv/items/<int:pk>/", views.ItemView.as_view(), name="item-detail"),
    path("inv/loans/", views.LoanListView.as_view(), name="loans"),
    path("inv/loans/<int:pk>/", views.LoanView.as_view(), name="loan-detail"),
    path(
        "inv/portions/<int:pk>/", views.ItemPortionView.as_view(), name="portion-detail"
    ),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/auth-signin/", views.AuthSignin.as_view(), name="signin"),
    path("accounts/logout/", views.user_logout_view, name="logout"),
    path("func/get_tree_data/", views.get_tree_data, name="gettreedata"),
]

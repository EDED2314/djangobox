from django.urls import path

from . import dashboard, views

urlpatterns = [
    path("", views.index, name="index"),
    path("inv/locations/", views.LocationListView.as_view(), name="locations"),
    path("inv/boxes/", views.BoxListView.as_view(), name="boxes"),
    path("inv/boxes/<slug:slug>/", views.BoxView.as_view(), name="box-detail"),
    path("inv/items/", views.ItemListView.as_view(), name="items"),
    path("inv/items/<int:pk>/", views.ItemView.as_view(), name="item-detail"),
    path("inv/loans/", views.LoanListView.as_view(), name="loans"),
    path("inv/loans/<slug:slug>/", views.LoanView.as_view(), name="loan-detail"),
    path(
        "inv/portions/<slug:slug>/",
        views.ItemPortionView.as_view(),
        name="portion-detail",
    ),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/auth-signin/", views.AuthSignin.as_view(), name="signin"),
    path("accounts/logout/", views.user_logout_view, name="logout"),
    path("func/get_tree_data/", dashboard.get_tree_data, name="gettreedata"),
    path(
        "func/box_selector/<int:targetId>/<str:type>",
        dashboard.box_selector,
        name="boxselector",
    ),
]

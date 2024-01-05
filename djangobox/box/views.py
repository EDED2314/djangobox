from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Location, Box, Item, Loan, ItemPortion
from .forms import LoginForm


def index(request):
    return render(request, "pages/dashboard.html")


class AuthSignin(auth_views.LoginView):
    template_name = "accounts/auth-signin.html"
    form_class = LoginForm
    success_url = "/"


@login_required(login_url="/accounts/auth-signin")
def profile(request):
    context = {"user": request.user}
    return render(request, "pages/user.html", context)


def user_logout_view(request):
    logout(request)
    return redirect("/accounts/auth-signin/")


class LocationListView(generic.ListView):
    model = Location
    context_object_name = "location_list"


class BoxListView(generic.ListView):
    model = Box


class BoxView(generic.DetailView):
    model = Box


class ItemListView(generic.ListView):
    model = Item


class ItemView(generic.DetailView):
    model = Item


class LoanListView(generic.ListView):
    model = Loan


class LoanView(generic.DetailView):
    model = Loan


class ItemPortionView(generic.DetailView):
    model = ItemPortion
    slug_url_kwarg = "slug"

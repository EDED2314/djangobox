from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Location, Box, Item, Loan, ItemPortion
from .forms import LoginForm
from django.db.models import Sum


def index(request):
    return render(request, "pages/dashboard.html", {"user": request.user})


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


class BoxListView(generic.ListView):
    model = Box
    paginate_by = 15

    def get_queryset(self):
        query_set = Box.objects.get_queryset().order_by("-created_at")
        return query_set


class BoxView(generic.DetailView):
    model = Box


class ItemListView(generic.ListView):
    model = Item
    paginate_by = 15

    def get_queryset(self):
        query_set = Item.objects.get_queryset().order_by("-name")
        return query_set

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        items_with_total_quantity = Item.objects.annotate(
            total_quantity=Sum("portions__qty")
        )

        context["item_list"] = items_with_total_quantity
        return context


class ItemView(generic.DetailView):
    model = Item


class LoanListView(generic.ListView):
    model = Loan
    paginate_by = 15

    def get_queryset(self):
        query_set = Loan.objects.get_queryset().order_by("-timestamp_borrow")
        return query_set


class LoanView(generic.DetailView):
    model = Loan


class ItemPortionView(generic.DetailView):
    model = ItemPortion

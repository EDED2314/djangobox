from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Location, Box, Item, Loan
from .forms import LoginForm


def get_sub_box_data(box):
    """Recursively gather data from sub-boxes."""
    box_data = {"name": box.name, "url": box.get_absolute_url(), "children": []}

    items = box.items.all()
    for item in items:
        item_data = {"name": item.name, "url": item.get_absolute_url(), "children": []}

        portions = item.portions.all()
        for portion in portions:
            portion_data = {"name": f"Portion: {portion.uuid}", "size": portion.qty}
            item_data["children"].append(portion_data)

        box_data["children"].append(item_data)

    subbox_data = []
    subboxes = box.subboxes.all()
    for subbox in subboxes:
        subbox_data.append(get_sub_box_data(subbox))

    box_data["children"].extend(subbox_data)

    return box_data


def get_tree_data(request):
    locations = Location.objects.all()
    tree_data = []

    for location in locations:
        location_data = {
            "name": location.name,
            "url": location.get_absolute_url(),
            "children": [],
        }

        boxes = location.boxes.all()
        for box in boxes:
            location_data["children"].append(get_sub_box_data(box))

        tree_data.append(location_data)

    # print(tree_data)
    return JsonResponse(tree_data, safe=False)


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

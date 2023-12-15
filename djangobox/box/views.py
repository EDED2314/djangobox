from django.shortcuts import render
from django.views import generic

from django.http import HttpResponse
from .models import Location, Box, Item


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class LocationListView(generic.ListView):
    model = Location


class LocationView(generic.DetailView):
    model = Location


class BoxListView(generic.ListView):
    model = Box


class BoxView(generic.DetailView):
    model = Box


class ItemListView(generic.ListView):
    model = Item


class ItemView(generic.DetailView):
    model = Item

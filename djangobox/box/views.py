from django.shortcuts import render
from django.views import generic

from django.http import HttpResponse
from models import Location


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class RoomListView(generic.ListView):
    model = Location


class RoomDetailView(generic.DetailView):
    model = Location

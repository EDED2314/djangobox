from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from django.urls import reverse


class User(AbstractUser):
    user_id = models.PositiveIntegerField(
        default=00000, validators=[MaxValueValidator(999999)], unique=True
    )

    def __str__(self):
        return self.username


class Location(models.Model):
    """A main location of some storage boxes

    e.g. Brook Storages, Room 102

    To access boxes inside this location:
    `location_boxes = location.boxes.all()`
    """

    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    roomcode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location-detail", args=[str(self.id)])


class Box(models.Model):
    """Storage Model

    name -- the name of the storage unit \n
    location -- the location in which it is stored \n
    boxes -- storage units within this box. \n

    To locate subboxes of a box:
    `sub_boxes = my_box.subboxes.all()`

    To locate boxes of a subbox:
    `boxes = sub_box.boxes.all()`
    """

    name = models.CharField(max_length=200)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="boxes"
    )
    boxes = models.ManyToManyField("Box", related_name="subboxes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("box-detail", args=[str(self.id)])


class Item(models.Model):
    """A item

    To access the `ItemPortion` list of this item:
    `portions = item.portions.all()`
    """

    # genearl fields
    name = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)

    # optional fields
    sku = models.CharField(max_length=100, default="", blank=True)
    mpn = models.CharField(max_length=100, default="", blank=True)
    upc = models.IntegerField(blank=True, null=True)

    # relations
    unit = models.ForeignKey("Unit", related_name="taggedItems")


class ItemPortion(models.Model):
    item = models.ForeignKey(Item, related_name="portions")
    qty = models.IntegerField(default=0, validators=[MinValueValidator(0)])


class Unit(models.Model):
    """A unit attributed to item it references e.g. bit, a drill bit

    To access the items that have this instance as a unit:
    `items = unit.taggedItems.all()`
    """

    unit_name = models.CharField(max_length=30)
    unit_description = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.unit_name

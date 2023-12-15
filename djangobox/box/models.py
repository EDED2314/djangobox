import logging

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from django.urls import reverse

from shortuuidfield import ShortUUIDField

import os
import barcode

from io import BytesIO
from django.core.files import File
from barcode.writer import ImageWriter
from barcode.errors import BarcodeError


class User(AbstractUser):
    """Custom user model with an additional user_id field."""

    user_id = models.PositiveIntegerField(
        default="00000", validators=[MaxValueValidator(999999)], unique=True
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

    To access subboxes of a box:
    `sub_boxes = my_box.subboxes.all()`

    To access boxes of a subbox:
    `boxes = sub_box.boxes.all()`

    To access the items in this box:
    `item_portions_in_this_box = box.items.all()`
    """

    name = models.CharField(max_length=200)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="boxes"
    )
    boxes = models.ManyToManyField("Box", related_name="subboxes", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("box-detail", args=[str(self.id)])


class Item(models.Model):
    """A item

    To access the `ItemPortion` list of this item:
    `portions = item.portions.all()`
    """

    name = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)

    barcode = models.ImageField(
        upload_to=settings.BARCODE_ROOT,
        blank=True,
        default=os.path.join(settings.BARCODE_ROOT, "barcode.png"),
    )

    sku = models.CharField(max_length=100, default="", blank=True)
    mpn = models.CharField(max_length=100, default="", blank=True)
    upc = models.IntegerField(blank=True, null=True)

    unit = models.ForeignKey(
        "Unit",
        on_delete=models.SET_NULL,
        related_name="tagged_items",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item-detail", args=[str(self.id)])


class ItemPortion(models.Model):
    """A portion/physical manifestation of an item."""

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="portions")
    qty = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    uuid = ShortUUIDField()

    box = models.ForeignKey(
        Box, on_delete=models.SET_NULL, related_name="items", null=True
    )

    def __str__(self):
        return f"Item:'{self.item.name}' in Box:'{self.box.name}'"

    def save(self, *args, **kwargs):
        """overrides the save function to add a barcode generation"""

        super().save(*args, **kwargs)

        try:
            file_name = f"item-{self.item.name}_pk{self.pk}.png"
            full_path = os.path.join(settings.BARCODE_ROOT, file_name)

            # Check if the file already exists before saving
            if not (os.path.isfile(full_path)):
                barclass = barcode.get_barcode_class("Code128")
                code = barclass(f"{self.uuid}", writer=ImageWriter())
                buffer = BytesIO()
                code.write(buffer)
                self.item.barcode.save(file_name, File(buffer), save=False)

        except BarcodeError as e:
            logger = logging.getLogger(__name__)
            logger.error(
                f"[ItemPortion uuid:{self.pk}]| Barcode generation failed for Item {self.item.name}: {e}"
            )

        return self

    def delete(self):
        """overrides the save function to add a barcode deletion"""
        file_name = f"item-{self.item.name}_pk{self.pk}.png"
        full_path = os.path.join(settings.BARCODE_ROOT, file_name)

        if os.path.isfile(full_path):
            os.remove(full_path)

        super().delete()


class Unit(models.Model):
    """A unit attributed to item it references e.g. bit, a drill bit

    To access the items that have this instance as a unit:
    `items = unit.tagged_items.all()`
    """

    unit_name = models.CharField(max_length=30)
    unit_description = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.unit_name

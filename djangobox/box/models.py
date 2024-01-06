from django.utils import timezone
import logging

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

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
        return reverse("locations")


class Box(models.Model):
    """Storage model

    To access subboxes of a box: (the boxes stored in my_box object)
    `sub_boxes = my_box.subboxes.all()`

    To access the items in this box:
    `item_portions_in_this_box = box.items.all()`
    """

    name = models.CharField(max_length=200)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="boxes", blank=True, null=True
    )
    box = models.ForeignKey(
        "Box", on_delete=models.SET_NULL, related_name="subboxes", blank=True, null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("box-detail", args=[str(self.id)])

    def clean(self):
        """
        Ensure that a box cannot reference itself as a subbox.
        """
        if self.box == self:
            raise ValidationError("A box cannot be a subbox of itself.")

    def save(self, *args, **kwargs):
        """
        Override the save method to call clean before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Item(models.Model):
    """An item model

    To access the `ItemPortion` list of this item:
    `portions = item.portions.all()`
    """

    name = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)

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
    slug = ShortUUIDField()

    box = models.ForeignKey(
        Box, on_delete=models.SET_NULL, related_name="items", null=True
    )

    barcode = models.ImageField(
        upload_to=settings.BARCODE_RELATIVE,
        blank=True,
        default=os.path.join(settings.BARCODE_ROOT, "notbarcode.png"),
    )

    def __str__(self):
        return f"Item:'{self.item.name}' in Box:'{self.box.name}'"

    def save(self, *args, **kwargs):
        """overrides the save function to add a barcode generation"""

        super().save(*args, **kwargs)

        try:
            file_name = f"item-{self.item.name.replace(' ', '_')}_pk{self.pk}.png"
            full_path = os.path.join(settings.BARCODE_ROOT, file_name)

            if not (os.path.isfile(full_path)):
                barclass = barcode.get_barcode_class("Code128")
                code = barclass(f"{self.slug}", writer=ImageWriter())
                buffer = BytesIO()
                code.write(buffer)
                self.barcode.save(file_name, File(buffer), save=True)

        except BarcodeError as e:
            logger = logging.getLogger(__name__)
            logger.error(
                f"[ItemPortion uuid:{self.slug}]| Barcode generation failed for Item {self.item.name}: {e}"
            )

        return self

    def delete(self):
        """overrides the save function to add a barcode deletion"""
        path = self.barcode.path
        if os.path.isfile(path) and "notbarcode" not in path:
            os.remove(path)

        super().delete()

    def get_absolute_url(self):
        return reverse("portion-detail", args=[str(self.slug)])


class Loan(models.Model):
    """A borrowed/returned instance that tracks item loans + transactions"""

    qty = models.IntegerField(validators=[MinValueValidator(1)])
    qty_returned = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, default=0
    )

    timestamp_borrow = models.DateTimeField(auto_now_add=True)
    timestamp_return = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
    )

    STATUS = (
        ("n", "None Returned"),
        ("p", "Partially Returned"),
        ("r", "Fully Returned"),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default="n",
        help_text="Loan status",
        editable=False,
    )

    item = models.ForeignKey(
        ItemPortion, on_delete=models.SET_NULL, related_name="loans", null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="loans",
        null=True,
    )

    class Meta:
        ordering = ["timestamp_borrow"]

    def __str__(self):
        return f"Loan of {self.qty} {self.item.item.name} to {self.user.username}"

    def save(self, *args, **kwargs):
        """
        Override the save method to check constraints on qty and qty_returned.
        """
        if self.qty_returned > self.qty:
            raise ValidationError("Returned quantity cannot exceed borrowed quantity.")

        if not self.pk:
            if self.qty > self.item.qty:
                raise ValidationError("Requested quantity exceeds available quantity.")

            self.item.qty -= self.qty
            self.item.save()

        elif self.pk:
            previous_state = Loan.objects.get(pk=self.pk)

            if previous_state.status == "r":
                raise ValidationError("Cannot modify a fully returned loan.")

            if self.qty_returned == self.qty:
                self.status = "r"
            elif self.qty_returned < self.qty and self.qty_returned > 0:
                self.status = "p"
            elif self.qty_returned == 0:
                self.status = "n"

            if self.status == "r":
                if self.qty_returned != self.qty:
                    raise ValidationError(
                        "Must fully return the items before marking the loan as fully returned."
                    )
                self.timestamp_return = timezone.now()

            if self.status == "p":
                if self.qty_returned == 0:
                    raise ValidationError(
                        "Must at least return a item before marking loan as partially returned."
                    )
                elif self.qty_returned == self.qty:
                    raise ValidationError(
                        "Must mark loan as 'r' if all items in loan are returned"
                    )

            if self.status == "n":
                if self.qty_returned != 0:
                    raise ValidationError(
                        "Must have no items returned in order to mark something as none returned."
                    )

            diff = self.qty_returned - previous_state.qty_returned
            self.item.qty += diff
            self.item.save()

        super().save(*args, **kwargs)

    def delete(self):
        """overrides the save function"""
        itemqtyleft = self.qty - self.qty_returned
        self.item.qty += itemqtyleft
        self.item.save()

        super().delete()

    def get_absolute_url(self):
        return reverse("loan-detail", args=[str(self.id)])


class Unit(models.Model):
    """A unit attributed to an item it references e.g. bit, a drill bit

    To access the items that have this instance as a unit:
    `items = unit.tagged_items.all()`
    """

    unit_name = models.CharField(max_length=30)
    unit_description = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.unit_name

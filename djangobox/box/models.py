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
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    roomcode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Location."""
        return reverse("location-detail", args=[str(self.id)])


class Box(models.Model):
    """DjangoBox's Storage Model

    name -- the name of the storage unit
    location -- the location in which it is stored
    boxes -- storage units within this box.
    """

    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    boxes = models.ManyToManyField("Box", related_name="subboxes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("box-detail", args=[str(self.id)])

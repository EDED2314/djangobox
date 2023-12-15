from django.test import TestCase
from django.urls import reverse

from .models import User, Location, Box, Item, ItemPortion, Unit


class ModelTests(TestCase):
    def setUp(self):
        # Create sample instances for testing
        self.user = User.objects.create(username="testuser", user_id=12345)
        self.location = Location.objects.create(name="Test Location")
        self.box = Box.objects.create(name="Test Box", location=self.location)
        self.item = Item.objects.create(name="Test Item")
        self.unit = Unit.objects.create(unit_name="Test Unit")

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "testuser")

    def test_location_str_method(self):
        self.assertEqual(str(self.location), "Test Location")

    def test_box_str_method(self):
        self.assertEqual(str(self.box), "Test Box")

    def test_item_str_method(self):
        self.assertEqual(str(self.item), "Test Item")

    def test_unit_str_method(self):
        self.assertEqual(str(self.unit), "Test Unit")

    def test_location_absolute_url(self):
        url = reverse("location-detail", args=[str(self.location.id)])
        self.assertEqual(self.location.get_absolute_url(), url)

    def test_box_absolute_url(self):
        url = reverse("box-detail", args=[str(self.box.id)])
        self.assertEqual(self.box.get_absolute_url(), url)

    def test_item_absolute_url(self):
        url = reverse("item-detail", args=[str(self.item.id)])
        self.assertEqual(self.item.get_absolute_url(), url)

    def test_item_portion_str_method(self):
        item_portion = ItemPortion.objects.create(
            item=self.item, qty=1, uuid="STRTEST", box=self.box
        )
        expected_str = f"Item:'Test Item' in Box:'Test Box'"
        self.assertEqual(str(item_portion), expected_str)
        item_portion.delete()

    def test_item_portion_save_method(self):
        item_portion = ItemPortion.objects.create(
            item=self.item, qty=1, uuid="SAVETEST", box=self.box
        )
        # Ensure barcode file is created
        self.assertTrue(item_portion.barcode.name)
        item_portion.delete()

    def test_item_portion_delete_method(self):
        item_portion = ItemPortion.objects.create(
            item=self.item, qty=1, uuid="DELTEST", box=self.box
        )
        file_path = item_portion.barcode.path
        # Ensure barcode file exists before deletion
        self.assertTrue(item_portion.barcode.storage.exists(file_path))
        item_portion.delete()
        # Ensure barcode file is deleted
        self.assertFalse(item_portion.barcode.storage.exists(file_path))

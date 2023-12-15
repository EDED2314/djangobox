from django.test import TestCase
from box.models import Location, Box, Item, ItemPortion, Unit


class ModelsTestCase(TestCase):
    def setUp(self):
        # Create test data for models
        self.location = Location.objects.create(name="Test Location")
        self.box = Box.objects.create(name="Test Box", location=self.location)
        self.unit = Unit.objects.create(unit_name="Test Unit")

    def test_location_str(self):
        self.assertEqual(str(self.location), "Test Location")

    def test_box_str(self):
        self.assertEqual(str(self.box), "Test Box")

    def test_item_str(self):
        item = Item.objects.create(name="Test Item", unit=self.unit)
        self.assertEqual(str(item), "Test Item")

    def test_item_portion_str(self):
        item_portion = ItemPortion.objects.create(
            item=Item.objects.create(name="Test Item"), box=self.box
        )
        self.assertEqual(str(item_portion), "Item:'Test Item' in Box:'Test Box'")

    def test_unit_str(self):
        self.assertEqual(str(self.unit), "Test Unit")

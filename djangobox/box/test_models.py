from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone


from .models import User, Location, Box, Item, ItemPortion, Unit, Loan


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", user_id=12345)
        self.location = Location.objects.create(name="Test Location")

        self.unit = Unit.objects.create(unit_name="Test Unit")

        self.box2 = Box.objects.create(name="Superglues", location=self.location)
        self.box1 = Box.objects.create(name="ca sprays", box=self.box2)
        self.box3 = Box.objects.create(name="Drills", location=self.location)
        self.wireBox = Box.objects.create(name="wires")

        self.item = Item.objects.create(name="Test Item")
        self.item_portion = ItemPortion.objects.create(
            item=self.item, qty=10, uuid="test-uuid"
        )

    def test_location_absolute_url(self):
        url = reverse("locations", args=[str(self.location.id)])
        self.assertEqual(self.location.get_absolute_url(), url)

    def test_box_foreignkey(self):
        self.assertEqual(self.box1.box.name, "Superglues")

    def test_boxes_subbox(self):
        self.assertEqual(list(self.box2.subboxes.all()), [self.box1])

    def test_box_absolute_url(self):
        url = reverse("box-detail", args=[str(self.box1.id)])
        self.assertEqual(self.box1.get_absolute_url(), url)

    def test_item_absolute_url(self):
        url = reverse("item-detail", args=[str(self.item.id)])
        self.assertEqual(self.item.get_absolute_url(), url)

    def test_item_portion_save_method(self):
        item_portion = ItemPortion.objects.create(
            item=self.item, qty=1, uuid="SAVETEST", box=self.box1
        )
        # Ensure barcode file is created
        self.assertTrue(item_portion.barcode.name)
        item_portion.delete()

    def test_item_portion_delete_method(self):
        item_portion = ItemPortion.objects.create(
            item=self.item, qty=1, uuid="DELTEST", box=self.box1
        )
        file_path = item_portion.barcode.path
        # Ensure barcode file exists before deletion
        self.assertTrue(item_portion.barcode.storage.exists(file_path))
        item_portion.delete()
        # Ensure barcode file is deleted
        self.assertFalse(item_portion.barcode.storage.exists(file_path))

    def test_loan_save_valid_qty(self):
        # Test saving a loan with a valid quantity
        loan = Loan.objects.create(
            qty=5,
            timestamp_borrow=timezone.now(),
            item=self.item_portion,
            user=self.user,
        )
        self.assertEqual(loan.qty, 5)  # Ensure the quantity is set correctly

    def test_loan_save_invalid_qty(self):
        # Test saving a loan with a quantity exceeding available quantity
        with self.assertRaises(ValidationError):
            Loan.objects.create(
                qty=15,  # This exceeds the available quantity (10)
                timestamp_borrow=timezone.now(),
                item=self.item_portion,
                user=self.user,
            )

    def test_loan_save_invalid_returned_qty(self):
        # Test saving a loan with returned quantity exceeding borrowed quantity
        with self.assertRaises(ValidationError):
            Loan.objects.create(
                qty=10,
                qty_returned=15,  # This exceeds the borrowed quantity (10)
                timestamp_borrow=timezone.now(),
                item=self.item_portion,
                user=self.user,
            )

    def test_loan_save_fully_returned(self):
        # Test saving a loan with status set to "Fully Returned"
        loan = Loan.objects.create(
            qty=5,
            qty_returned=5,
            timestamp_borrow=timezone.now(),
            timestamp_return=timezone.now(),
            status="r",
            item=self.item_portion,
            user=self.user,
        )

        with self.assertRaises(ValidationError):
            loan.save()

    def test_loan_save_invalid_returned_qty_with_status(self):
        # Test saving a loan with returned quantity exceeding borrowed quantity and status set to "Fully Returned"
        with self.assertRaises(ValidationError):
            Loan.objects.create(
                qty=10,
                qty_returned=15,
                timestamp_borrow=timezone.now(),
                timestamp_return=timezone.now(),
                status="r",
                item=self.item_portion,
                user=self.user,
            )

    def test_loan_create(self):
        jumperwires = Item.objects.create(name="Red Jumper Wires")
        jumperwiresPortion = ItemPortion.objects.create(
            item=jumperwires, qty=20, box=self.wireBox
        )
        wireLoan = Loan.objects.create(
            qty=10,
            item=jumperwiresPortion,
            user=self.user,
            timestamp_borrow=timezone.now(),
        )
        wireLoan.qty_returned = 10
        wireLoan.status = "r"
        wireLoan.save()

        with self.assertRaises(ValidationError):
            wireLoan.status = "p"
            wireLoan.save()

        jumperwiresPortion.delete()
        self.assertFalse(
            jumperwiresPortion.barcode.storage.exists(jumperwiresPortion.barcode.path)
        )

"""Test models"""
from decimal import Decimal

from django.test import TestCase

from model_bakery import baker


class TestLocationModels(TestCase):
    """Test class for purchase models."""

    def test_model_methods(self):
        """Test model methods."""
        business = baker.make("locations.Business", name="Abc Ltd")
        location = baker.make("locations.Location", name="Voi")
        department = baker.make("locations.Department", name="Science")
        self.assertEqual("Abc Ltd", business.__str__())
        self.assertEqual("Voi", location.__str__())
        self.assertEqual("Science", department.__str__())


class TestPurchaseModels(TestCase):
    """Test class for purchase models."""

    def test_model_methods(self):
        """Test model methods."""
        requisition = baker.make(
            "purchases.Requisition",
            title="Super Duper Important",
            date_placed="2019-06-24",
            date_required="2019-06-24",
        )
        self.assertEqual(
            f"#{requisition.id} Super Duper Important", requisition.__str__()
        )
        requisition_item = baker.make(
            "purchases.RequisitionLineItem",
            item="Pen",
            quantity=2,
            internal_price=20,
            requisition=requisition,
        )
        self.assertEqual(
            f"{requisition_item.item} - #{requisition_item.requisition}",
            requisition_item.__str__(),
        )
        baker.make(
            "purchases.RequisitionLineItem",
            _quantity=1,
            item="Ink",
            quantity=3,
            internal_price=19,
            requisition=requisition,
        )

        self.assertEqual(Decimal(0), requisition.total)
        self.assertEqual(Decimal(97), requisition.get_total())
        requisition.set_total()
        requisition.refresh_from_db()
        self.assertEqual(Decimal(97), requisition.total)

"""Test models"""
from decimal import Decimal

from django.test import TestCase

from model_mommy import mommy


class TestPurchaseModels(TestCase):
    """
    Test class for purchase models
    """

    def test_model_methods(self):
        """Test model methods"""
        requisition = mommy.make(
            "purchases.Requisition",
            date_placed="2019-06-24",
            date_required="2019-06-24",
        )
        self.assertEqual(f"{requisition.id}", requisition.__str__())
        requisition_item = mommy.make(
            "purchases.RequisitionLineItem",
            item="Pen",
            quantity=2,
            price=20,
            requisition=requisition,
        )
        self.assertEqual(
            f"{requisition_item.item} - #{requisition_item.requisition}",
            requisition_item.__str__(),
        )
        mommy.make(
            "purchases.RequisitionLineItem",
            _quantity=1,
            item="Ink",
            quantity=3,
            price=19,
            requisition=requisition,
        )

        self.assertEqual(Decimal(97), requisition.get_total())

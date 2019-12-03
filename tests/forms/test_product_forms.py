"""Module for product form tests."""
from django.test import RequestFactory, TestCase

from tiny_erp.apps.products.forms import SupplierForm


class TestProductForms(TestCase):
    """Test class for product forms."""

    def setUp(self):
        """Setup test class."""
        self.factory = RequestFactory()

    def test_supplier_form(self):
        """Test SupplierForm."""
        data = {
            "name": "Umbrella Inc",
            "contact_person": "Marvin",
            "emails": "a@example.com,b@example.com",
            "phones": "+254724770584",
        }
        form = SupplierForm(data=data)
        self.assertTrue(form.is_valid())
        supplier = form.save()
        self.assertEqual("Umbrella Inc", supplier.name)
        self.assertEqual("Marvin", supplier.contact_person)
        self.assertEqual(["a@example.com", "b@example.com"], supplier.emails)
        self.assertEqual(["+254724770584"], supplier.phones)

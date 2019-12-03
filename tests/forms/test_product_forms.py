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
            "phones": "+254722000000",
        }
        form = SupplierForm(data=data)
        self.assertTrue(form.is_valid())
        supplier = form.save()
        self.assertEqual("Umbrella Inc", supplier.name)
        self.assertEqual("Marvin", supplier.contact_person)
        self.assertEqual(["a@example.com", "b@example.com"], supplier.emails)
        self.assertEqual(["+254722000000"], supplier.phones)

        update_data = {
            "name": "Umbrella Inc",
            "contact_person": "Alice",
            "emails": "b@example.com",
            "phones": "+254711000000,+254722000000",
        }

        form = SupplierForm(instance=supplier, data=update_data)
        self.assertTrue(form.is_valid())
        form.save()
        supplier.refresh_from_db()
        self.assertEqual("Umbrella Inc", supplier.name)
        self.assertEqual("Alice", supplier.contact_person)
        self.assertEqual(["b@example.com"], supplier.emails)
        self.assertEqual(["+254711000000", "+254722000000"], supplier.phones)

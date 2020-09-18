"""Module for product form tests."""
from decimal import Decimal

from django.conf import settings
from django.test import RequestFactory

from model_bakery import baker
from prices import Money
from snapshottest.django import TestCase

from tiny_erp.apps.products.forms import ProductForm, SupplierForm


class TestProductForms(TestCase):
    """Test class for product forms."""

    maxDiff = None

    def setUp(self):
        """Set up test class."""
        self.supplier = baker.make("products.Supplier", name="X Inc")
        self.supplier2 = baker.make("products.Supplier", name="Y Inc")
        self.unit = baker.make("products.MeasurementUnit", name="g")
        self.unit2 = baker.make("products.MeasurementUnit", name="l")
        self.category = baker.make("products.ProductCategory", name="a")
        self.category2 = baker.make("products.ProductCategory", name="b")
        self.factory = RequestFactory()

    def test_supplier_form(self):
        """Test SupplierForm."""
        # test empty form output
        self.assertMatchSnapshot(SupplierForm().as_p())

        # test form when creating
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

        # test form when updating
        update_data = {
            "name": "Umbrella Inc",
            "contact_person": "Alice",
            "emails": "b@example.com",
            "phones": "+254711000000, +254722000000",  # notice the empty space
        }

        form = SupplierForm(instance=supplier, data=update_data)
        self.assertMatchSnapshot(form.as_p())
        self.assertTrue(form.is_valid())
        form.save()
        supplier.refresh_from_db()
        self.assertEqual("Umbrella Inc", supplier.name)
        self.assertEqual("Alice", supplier.contact_person)
        self.assertEqual(["b@example.com"], supplier.emails)
        self.assertEqual(["+254711000000", "+254722000000"], supplier.phones)

        # test empty phone
        data = {
            "name": "Umbrella Inc",
            "contact_person": "Marvin",
            "emails": "a@example.com,b@example.com",
            "phones": "",
        }
        form = SupplierForm(data=data)
        self.assertTrue(form.is_valid())
        supplier = form.save()
        self.assertEqual("Umbrella Inc", supplier.name)
        self.assertEqual("Marvin", supplier.contact_person)
        self.assertEqual(["a@example.com", "b@example.com"], supplier.emails)
        self.assertEqual([], supplier.phones)

        # test empty email
        data = {
            "name": "Umbrella Inc",
            "contact_person": "Marvin",
            "emails": "",
            "phones": "+254722000000",
        }
        form = SupplierForm(data=data)
        self.assertTrue(form.is_valid())
        supplier = form.save()
        self.assertEqual("Umbrella Inc", supplier.name)
        self.assertEqual("Marvin", supplier.contact_person)
        self.assertEqual([], supplier.emails)
        self.assertEqual(["+254722000000"], supplier.phones)

    def test_supplier_form_validation(self):
        """Test SupplierForm validation."""
        # test name validation
        data = {
            "name": "",
            "contact_person": "Marvin",
            "emails": "a@example.com,b@example.com",
            "phones": "+254711000000",
        }
        form = SupplierForm(data=data)
        form.full_clean()
        self.assertFalse(form.is_valid())
        self.assertDictEqual({"name": ["This field is required."]}, form.errors)

        # test contact_person validation
        data = {
            "name": "Umbrella Inc",
            "contact_person": "",
            "emails": "a@example.com,b@example.com",
            "phones": "+254711000000",
        }
        form = SupplierForm(data=data)
        form.full_clean()
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            {"contact_person": ["This field is required."]}, form.errors
        )

        # test phone validation
        data = {
            "name": "Umbrella Inc",
            "contact_person": "Marvin",
            "emails": "a@example.com,b@example.com",
            "phones": "+254722000000, +2547999999999999",
        }
        form = SupplierForm(data=data)
        form.full_clean()
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            {"phones": ["The phone number entered is not valid."]}, form.errors
        )

        # test email validation
        data = {
            "name": "Umbrella Inc",
            "contact_person": "Marvin",
            "emails": "42",
            "phones": "+254722000000",
        }
        form = SupplierForm(data=data)
        form.full_clean()
        self.assertFalse(form.is_valid())
        self.assertDictEqual({"emails": ["Enter a valid email address."]}, form.errors)

        # test that one of email or phone is required
        data = {"name": "Umbrella Inc", "contact_person": "Marvin", "emails": ""}
        form = SupplierForm(data=data)
        form.full_clean()
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            {
                "emails": ["Provide a phone number or an email address."],
                "phones": ["Provide a phone number or an email address."],
            },
            form.errors,
        )

    def test_product_form(self):
        """Test ProductForm."""
        # test form when creating
        data = {
            "name": "Pen",
            "sku": "pen-1",
            "description": "A pen",
            "unit": self.unit.id,
            "category": [self.category.id],
            "supplier": self.supplier.id,
            "price_0": 20,
            "price_1": "KES",
        }
        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual("Pen", product.name)
        self.assertEqual("pen-1", product.sku)
        self.assertEqual("A pen", product.description)
        self.assertEqual(self.unit, product.unit)
        self.assertEqual(self.category, product.category.first())
        self.assertEqual(self.supplier, product.supplier)
        self.assertEqual(Money("20", "KES"), product.amount)
        self.assertEqual(settings.TINY_ERP_DEFAULT_CURRENCY, product.currency)
        self.assertEqual(Decimal(20), product.internal_amount)

        # test form when updating
        data = {
            "name": "Nice Pen",
            "sku": "pen-1-1",
            "description": "A nice pen",
            "unit": self.unit2.id,
            "category": [self.category2],
            "supplier": self.supplier2.id,
            "price_0": 25,
            "price_1": "KES",
        }
        form = ProductForm(instance=product, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        product.refresh_from_db()
        self.assertEqual("Nice Pen", product.name)
        self.assertEqual("pen-1-1", product.sku)
        self.assertEqual("A nice pen", product.description)
        self.assertEqual(self.unit2, product.unit)
        self.assertEqual(self.category2, product.category.first())
        self.assertEqual(self.supplier2, product.supplier)
        self.assertEqual(Money("25", "KES"), product.amount)
        self.assertEqual(settings.TINY_ERP_DEFAULT_CURRENCY, product.currency)
        self.assertEqual(Decimal(25), product.internal_amount)

    def test_product_form_validation(self):
        """Test ProductForm validation."""
        # test price
        data = {
            "name": "Pen",
            "sku": "pen-2",
            "description": "A pen",
            "unit": self.unit.id,
            "category": [self.category.id],
            "supplier": self.supplier.id,
            "price_0": -20,
            "price_1": "KES",
        }
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            {"price": ["Ensure this value is greater than or equal to KES0.00."]},
            form.errors,
        )

        # test required fields
        for field in ["category", "name", "unit"]:
            data = {
                "name": "Pen",
                "sku": "pen-3",
                "description": "A pen",
                "unit": self.unit.id,
                "category": [self.category.id],
                "supplier": self.supplier.id,
                "price_0": 20,
                "price_1": "KES",
            }
            data[field] = ""
            form = ProductForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertDictEqual({field: ["This field is required."]}, form.errors)

        # test price required
        for field in ["price_0", "price_1"]:
            data = {
                "name": "Pen",
                "sku": "pen-4",
                "description": "A pen",
                "unit": self.unit.id,
                "category": [self.category.id],
                "supplier": self.supplier.id,
                "price_0": 20,
                "price_1": "KES",
            }
            data[field] = ""
            form = ProductForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertDictEqual({"price": ["This field is required."]}, form.errors)

        # test related fields
        data = {
            "name": "Pen",
            "sku": "pen-5",
            "description": "A pen",
            "unit": "1337",
            "category": [1337],
            "supplier": "1337",
            "price_0": 20,
            "price_1": "KES",
        }
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            {
                "category": [
                    "Select a valid choice. 1337 is not one of the available choices."
                ],
                "supplier": [
                    "Select a valid choice. That choice is not one of the available choices."  # noqa  # pylint: disable=line-too-long
                ],
                "unit": [
                    "Select a valid choice. That choice is not one of the available choices."  # noqa  # pylint: disable=line-too-long
                ],
            },
            form.errors,
        )

        # test unique fields
        product = baker.make(
            "products.product",
            name="Book",
            internal_amount=99,
            id=123,
            sku="bk1",
            unit=baker.make("products.MeasurementUnit", name="Box", symbol="box"),
            supplier=baker.make("products.Supplier", name="GAP"),
        )
        data = {
            "name": "Pen",
            "sku": product.sku,
            "description": "A pen",
            "unit": self.unit.id,
            "category": [self.category.id],
            "supplier": self.supplier.id,
            "price_0": 20,
            "price_1": "KES",
        }
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            {"sku": ["Product with this SKU already exists."]}, form.errors
        )

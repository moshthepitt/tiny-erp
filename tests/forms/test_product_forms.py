"""Module for product form tests."""
from decimal import Decimal

from django.conf import settings
from django.test import RequestFactory, TestCase

from model_mommy import mommy
from prices import Money

from tiny_erp.apps.products.forms import ProductForm, SupplierForm

CREATE_SUPPLIER_FORM = """
<p>
    <label for="id_name">Name:</label>
    <input type="text" name="name" maxlength="2000" required id="id_name">
</p>
<p>
    <label for="id_contact_person">Contact Person:</label>
    <input type="text" name="contact_person" maxlength="2000" required id="id_contact_person">
</p>
<p>
    <label for="id_emails">Email Address(es):</label>
    <textarea name="emails" cols="40" rows="2" id="id_emails"></textarea>
    <span class="helptext">Enter a comma-separated list of email addresses</span></p>
<p>
    <label for="id_phones">Phone Number(s):</label>
    <textarea name="phones" cols="40" rows="2" id="id_phones"></textarea>
    <span class="helptext">Enter a comma-separated list of phone numbers</span>
</p>
"""  # noqa

UPDATE_SUPPLIER_FORM = """
<p>
    <label for="id_name">Name:</label>
    <input type="text" name="name" value="Umbrella Inc" maxlength="2000" required id="id_name">
</p>
<p>
    <label for="id_contact_person">Contact Person:</label>
    <input type="text" name="contact_person" value="Alice" maxlength="2000" required id="id_contact_person">
</p>
<p>
    <label for="id_emails">Email Address(es):</label>
    <textarea name="emails" cols="40" rows="2" id="id_emails">b@example.com</textarea>
    <span class="helptext">Enter a comma-separated list of email addresses</span></p>
<p>
    <label for="id_phones">Phone Number(s):</label>
    <textarea name="phones" cols="40" rows="2" id="id_phones">+254711000000, +254722000000</textarea>
    <span class="helptext">Enter a comma-separated list of phone numbers</span>
</p>
"""  # noqa


class TestProductForms(TestCase):
    """Test class for product forms."""

    maxDiff = None

    def setUp(self):
        """Setup test class."""
        self.supplier = mommy.make("products.Supplier", name="X Inc")
        self.supplier2 = mommy.make("products.Supplier", name="Y Inc")
        self.unit = mommy.make("products.MeasurementUnit", name="g")
        self.unit2 = mommy.make("products.MeasurementUnit", name="l")
        self.category = mommy.make("products.ProductCategory", name="a")
        self.category2 = mommy.make("products.ProductCategory", name="b")
        self.factory = RequestFactory()

    def test_supplier_form(self):
        """Test SupplierForm."""
        # test empty form output
        self.assertHTMLEqual(CREATE_SUPPLIER_FORM, SupplierForm().as_p())

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
        self.assertHTMLEqual(UPDATE_SUPPLIER_FORM, form.as_p())
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
        """Test SupplierForm vaidation."""

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
            "description": "A pen",
            "unit": self.unit.id,
            "category": [self.category.id],
            "supplier": [self.supplier.id],
            "price_0": 20,
            "price_1": "KES",
        }
        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual("Pen", product.name)
        self.assertEqual("A pen", product.description)
        self.assertEqual(self.unit, product.unit)
        self.assertEqual(self.category, product.category.first())
        self.assertEqual(self.supplier, product.supplier.first())
        self.assertEqual(Money("20", "KES"), product.amount)
        self.assertEqual(settings.TINY_ERP_DEFAULT_CURRENCY, product.currency)
        self.assertEqual(Decimal(20), product.internal_amount)

        # test form when updating
        data = {
            "name": "Nice Pen",
            "description": "A nice pen",
            "unit": self.unit2.id,
            "category": [self.category2],
            "supplier": [self.supplier.id, self.supplier2.id],
            "price_0": 25,
            "price_1": "KES",
        }
        form = ProductForm(instance=product, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        product.refresh_from_db()
        self.assertEqual("Nice Pen", product.name)
        self.assertEqual("A nice pen", product.description)
        self.assertEqual(self.unit2, product.unit)
        self.assertEqual(self.category2, product.category.first())
        self.assertEqual([self.supplier, self.supplier2], list(product.supplier.all()))
        self.assertEqual(Money("25", "KES"), product.amount)
        self.assertEqual(settings.TINY_ERP_DEFAULT_CURRENCY, product.currency)
        self.assertEqual(Decimal(25), product.internal_amount)

    def test_product_form_validation(self):
        """Test ProductForm validation."""

        # test price
        data = {
            "name": "Pen",
            "description": "A pen",
            "unit": self.unit.id,
            "category": [self.category.id],
            "supplier": [self.supplier.id],
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
                "description": "A pen",
                "unit": self.unit.id,
                "category": [self.category.id],
                "supplier": [self.supplier.id],
                "price_0": 20,
                "price_1": "KES",
            }
            data[field] = ""
            form = ProductForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertDictEqual({field: ["This field is required."]}, form.errors)

        # test price
        for field in ["price_0", "price_1"]:
            data = {
                "name": "Pen",
                "description": "A pen",
                "unit": self.unit.id,
                "category": [self.category.id],
                "supplier": [self.supplier.id],
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
            "description": "A pen",
            "unit": "1337",
            "category": [1337],
            "supplier": ["1337"],
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
                    "Select a valid choice. 1337 is not one of the available choices."
                ],
                "unit": [
                    "Select a valid choice. That choice is not one of the available choices."  # noqa  # pylint: disable=line-too-long
                ],
            },
            form.errors,
        )

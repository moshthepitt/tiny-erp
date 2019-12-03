"""Module for product form tests."""
from django.test import RequestFactory, TestCase

from tiny_erp.apps.products.forms import SupplierForm

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

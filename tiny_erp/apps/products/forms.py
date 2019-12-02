"""forms module for Products."""
from django import forms
from django.core.validators import validate_email
from django.utils.translation import ugettext as _

from phonenumber_field.validators import validate_international_phonenumber

from tiny_erp.apps.products.models import Supplier


class MultiInputField(forms.Field):
    """Base class for fields that take comma separated lists."""

    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(",")

    def validate(self, value):
        raise NotImplementedError


class MultiEmailField(MultiInputField):
    """Form field that takes comma separated list of emails."""

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)


class MultiPhoneField(MultiInputField):
    """Form field that takes comma separated list of phone numbers."""

    def validate(self, value):
        """Check if value consists only of valid phone numbers."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for phone in value:
            validate_international_phonenumber(phone)


class SupplierForm(forms.ModelForm):
    """Form definition for Supplier."""

    emails = MultiEmailField(
        label=_("Email Address(es)"),
        help_text=_("Enter a comma-seprated list of email addresses"),
        required=False,
    )
    phones = MultiPhoneField(
        label=_("Phone Number(s)"),
        help_text=_("Enter a comma-seprated list of phone numbers"),
        required=False,
    )

    class Meta:
        """Meta definition for Supplierform."""

        model = Supplier
        fields = ["name", "contact_person", "emails", "phones"]

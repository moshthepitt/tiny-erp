"""forms module for Products."""
from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.utils.translation import ugettext as _

from django_prices.forms import MoneyField
from django_prices.validators import MinMoneyValidator
from phonenumber_field.validators import validate_international_phonenumber
from prices import Money

from tiny_erp.apps.products.models import Product, Supplier


class MultiInputField(forms.Field):
    """Base class for fields that take comma separated lists."""

    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(",")


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


class MiniTextarea(forms.Textarea):
    """Vertically shorter version of textarea widget."""

    rows = 2

    def __init__(self, attrs=None):
        super().__init__({"rows": self.rows})


class SupplierForm(forms.ModelForm):
    """Form definition for Supplier."""

    emails = MultiEmailField(
        label=_("Email Address(es)"),
        help_text=_("Enter a comma-separated list of email addresses"),
        required=False,
        widget=MiniTextarea,
    )
    phones = MultiPhoneField(
        label=_("Phone Number(s)"),
        help_text=_("Enter a comma-separated list of phone numbers"),
        required=False,
        widget=MiniTextarea,
    )

    class Meta:
        """Meta definition for Supplierform."""

        model = Supplier
        fields = ["name", "contact_person", "emails", "phones"]


class ProductForm(forms.ModelForm):
    """Form definition for Product."""

    price = MoneyField(
        label=_("Price"),
        required=True,
        available_currencies=settings.TINY_ERP_AVAILABLE_CURRENCIES,
        max_digits=9,
        decimal_places=2,
        validators=[MinMoneyValidator(Money(0, settings.TINY_ERP_DEFAULT_CURRENCY))],
    )

    class Meta:
        """Meta definition for Productform."""

        model = Product
        fields = ["name", "description", "unit", "category", "supplier"]

    def save(self, commit=True):
        """Custom save method."""
        product = super().save()
        # deal with price
        product.internal_amount = self.cleaned_data["price"].amount
        product.currency = self.cleaned_data["price"].currency
        product.save()
        return product

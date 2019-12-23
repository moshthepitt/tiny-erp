"""models module for products app."""
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext as _

from vega_admin.mixins import TimeStampedModel

from phonenumber_field.modelfields import PhoneNumberField

from tiny_erp.abstract_models import MoneyModel


class Supplier(TimeStampedModel):
    """Model definition for Supplier."""

    name = models.CharField(_("Name"), max_length=2000)
    contact_person = models.CharField(_("Contact Person"), max_length=2000)
    emails = ArrayField(
        models.EmailField(_("Email Address")),
        verbose_name=_("Email Address(es)"),
        blank=True,
        default=list,
    )
    phones = ArrayField(
        PhoneNumberField(_("Telephone Number")),
        verbose_name=_("Phone number(s)"),
        blank=True,
        default=list,
    )

    class Meta:
        """Meta definition for Supplier."""

        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        """Unicode representation of Supplier."""
        return self.name


class MeasurementUnit(TimeStampedModel):
    """Model definition for MeasurementUnit."""

    name = models.CharField(_("Name"), max_length=2000, help_text=_("e.g. Kilogram"))
    symbol = models.CharField(
        _("Symbol"),
        db_index=True,
        max_length=2000,
        help_text=_("e.g. l which is the symbol for litre"),
    )
    description = models.TextField(_("Description"), blank=True, default="")

    class Meta:
        """Meta definition for MeasurementUnit."""

        verbose_name = _("Measurement Unit")
        verbose_name_plural = _("Measurement Units")

    def __str__(self):
        """Unicode representation of MeasurementUnit."""
        return self.name


class ProductCategory(TimeStampedModel):
    """Model definition for ProductCategory."""

    name = models.CharField(_("Name"), max_length=2000)
    description = models.TextField(_("Description"), blank=True, default="")

    class Meta:
        """Meta definition for ProductCategory."""

        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        """Unicode representation of ProductCategory."""
        return self.name


class Product(TimeStampedModel, MoneyModel):
    """Model definition for Product."""

    name = models.CharField(_("Name"), max_length=2000)
    sku = models.CharField(
        _("SKU"),
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        db_index=True,
        help_text=_("Stock Keeping Unit or Product Code"),
    )
    description = models.TextField(_("Description"), blank=True, default="")
    unit = models.ForeignKey(
        MeasurementUnit, verbose_name=_("Measurement Unit"), on_delete=models.PROTECT
    )
    category = models.ManyToManyField(ProductCategory, verbose_name=_("Category"))
    supplier = models.ForeignKey(
        Supplier, verbose_name=_("Supplier"), on_delete=models.PROTECT
    )

    class Meta:
        """Meta definition for Product."""

        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        """Unicode representation of Product."""
        return self.name

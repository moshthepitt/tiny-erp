"""module for abstract models."""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from vega_admin.mixins import TimeStampedModel

from django_prices.models import MoneyField


class AbstractEntity(models.Model):
    """Model definition for AbstractEntity."""

    name = models.CharField(_("Name"), max_length=255)
    active = models.BooleanField(_("Active"), default=True, blank=True)

    class Meta:
        """Meta definition for AbstractEntity."""

        abstract = True

    def __str__(self):
        """Unicode representation of name."""
        return self.name


class MoneyModel(models.Model):
    """Model definition for item with moneyfield."""

    currency = models.CharField(
        _("Currency"),
        max_length=3,
        choices=getattr(
            settings, "TINY_ERP_AVAILABLE_CURRENCIES", [("KES", "Kenya Shilling")]
        ),
        default=getattr(settings, "TINY_ERP_DEFAULT_CURRENCY", "KES"),
        db_index=True,
    )
    internal_amount = models.DecimalField(
        _("Price"), max_digits=64, decimal_places=2, default=0
    )
    amount = MoneyField(
        verbose_name=_("Price"),
        amount_field="internal_amount",
        currency_field="currency",
    )

    class Meta:
        """Meta definition for MoneyModel."""

        abstract = True


class AbstractLineItem(MoneyModel):
    """Model definition for abstract line item."""

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    quantity = models.DecimalField(
        _("Quantity"), max_digits=64, decimal_places=2, default=1
    )
    internal_price = models.DecimalField(
        _("Price"), help_text=_("The price per item"), max_digits=64, decimal_places=2
    )
    price = MoneyField(
        verbose_name=_("Price"),
        amount_field="internal_price",
        currency_field="currency",
    )

    # remove fields from base model class
    internal_amount = None
    amount = None

    def _get_total(self):
        """Get the total for this line item.

        Returns:
            Decimal -- the total for this line item
        """
        return self.internal_price * self.quantity

    @property
    def total(self):
        """Get the total for this line item.

        Returns:
            Decimal -- the total for this line item
        """
        return self._get_total()

    class Meta:
        """Meta definition for AbstractLineItem."""

        abstract = True


class TimeStampedAbstractEntity(TimeStampedModel, AbstractEntity):
    """Model definition for TimeStampedAbstractEntity."""

    class Meta:
        """Meta definition for TimeStampedAbstractEntity."""

        abstract = True


class TimeStampedAbstractLineItem(TimeStampedModel, AbstractLineItem):
    """Model definition for AbstractLineItem."""

    class Meta:
        """Meta definition for AbstractLineItem."""

        abstract = True

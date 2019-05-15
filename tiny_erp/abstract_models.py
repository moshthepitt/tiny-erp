"""module for abstract models"""
from django.db import models
from django.utils.translation import ugettext as _

from small_small_hr.models import TimeStampedModel


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


class AbstractLineItem(models.Model):
    """Model definition for abstract line item"""

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_('Description'), blank=True, default='')
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    price = models.DecimalField(
        _("Price"), help_text=_("The price per item"), max_digits=64,
        decimal_places=2)

    def _get_total(self):
        """Get the total for this line item

        Returns:
            Decimal -- the total for this line item
        """
        return self.price * self.quantity

    @property
    def total(self):
        """the total for this line item

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

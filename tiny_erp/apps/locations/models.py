"""Models module for locations app"""
from django.utils.translation import ugettext as _

from tiny_erp.abstract_models import TimeStampedAbstractEntity


class Business(TimeStampedAbstractEntity):
    """Model definition for Business."""

    class Meta:
        """Meta definition for Location."""

        verbose_name = _("Business")
        verbose_name_plural = _("Businesses")
        abstract = False


class Department(TimeStampedAbstractEntity):
    """Model definition for Department."""

    class Meta:
        """Meta definition for Location."""

        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        abstract = False


class Location(TimeStampedAbstractEntity):
    """Model definition for Location."""

    class Meta:
        """Meta definition for Location."""

        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        abstract = False

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


class TimeStampedAbstractEntity(TimeStampedModel, AbstractEntity):
    """Model definition for Business."""

    class Meta:
        """Meta definition for Location."""
        abstract = True

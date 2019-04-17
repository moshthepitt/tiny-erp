"""Models module for locations app"""
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from small_small_hr.models import TimeStampedModel


class Requisition(TimeStampedModel):
    """Model definition for Requisition."""
    APPROVED = '1'
    REJECTED = '2'
    PENDING = '3'

    STATUS_CHOICES = (
        (APPROVED, _('Approved')),
        (PENDING, _('Pending')),
        (REJECTED, _('Rejected'))
    )

    name = models.CharField(_("Title"), max_length=255)
    staff = models.ForeignKey(
        settings.USERPROFILE_MODEL, verbose_name=_('Staff Member'),
        on_delete=models.PROTECT)
    business = models.ForeignKey("tiny_erp.apps.locations.Business",
                                 verbose_name=_('Business'),
                                 on_delete=models.PROTECT)
    location = models.ForeignKey("tiny_erp.apps.locations.Location",
                                 verbose_name=_('Location'),
                                 on_delete=models.PROTECT)
    department = models.ForeignKey("tiny_erp.apps.locations.Department",
                                   verbose_name=_('Department'),
                                   on_delete=models.PROTECT)
    reason = models.TextField(_('Reason'), blank=False, default='')
    status = models.CharField(
        _('Status'), max_length=1, choices=STATUS_CHOICES, default=PENDING,
        blank=True, db_index=True)
    comments = models.TextField(_('Comments'), blank=True, default='')
    date_placed = models.DateField(_("Date Placed"))
    date_required = models.DateField(_("Date Required"))

    class Meta:
        """Meta definition for Requisition."""

        verbose_name = _('Requisition')
        verbose_name_plural = _('Requisitions')

    def __str__(self):
        """Unicode representation of Requisition."""
        return self.name

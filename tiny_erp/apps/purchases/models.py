"""Models module for locations app"""
from django.db import models
from django.utils.translation import ugettext as _

from small_small_hr.models import TimeStampedModel

from tiny_erp.abstract_models import TimeStampedAbstractLineItem
from tiny_erp.apps.locations.models import Business, Department, Location


# pylint: disable=no-member
class Requisition(TimeStampedModel):
    """Model definition for Requisition."""

    APPROVED = "1"
    REJECTED = "2"
    PENDING = "3"

    STATUS_CHOICES = (
        (APPROVED, _("Approved")),
        (PENDING, _("Pending")),
        (REJECTED, _("Rejected")),
    )

    staff = models.ForeignKey(
        "small_small_hr.StaffProfile",
        verbose_name=_("Staff Member"),
        on_delete=models.PROTECT,
    )
    business = models.ForeignKey(
        Business, verbose_name=_("Business"), on_delete=models.PROTECT
    )
    location = models.ForeignKey(
        Location, verbose_name=_("Location"), on_delete=models.PROTECT
    )
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.PROTECT
    )
    reason = models.TextField(_("Reason"), blank=False, default="")
    status = models.CharField(
        _("Status"),
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING,
        blank=True,
        db_index=True,
    )
    comments = models.TextField(_("Comments"), blank=True, default="")
    date_placed = models.DateField(_("Date Placed"))
    date_required = models.DateField(_("Date Required"))
    total = models.DecimalField(
        _("Total"), max_digits=64, decimal_places=2, blank=True, default=0
    )

    class Meta:
        """Meta definition for Requisition."""

        verbose_name = _("Requisition")
        verbose_name_plural = _("Requisitions")

    def get_total(self):
        """Get the total amount"""
        agg = RequisitionLineItem.objects.filter(requisition=self).aggregate(
            total=models.Sum(models.F("price") * models.F("quantity"))
        )
        return agg["total"]

    def set_total(self):
        """Save's the total to the DB"""
        self.total = self.get_total()
        self.save()

    def __str__(self):
        """Unicode representation of Requisition."""
        return f"{self.id}"


class RequisitionLineItem(TimeStampedAbstractLineItem):
    """Model definition for RequisitionLineItem."""

    requisition = models.ForeignKey(
        Requisition, verbose_name=_("Requisition"), on_delete=models.CASCADE
    )
    item = models.CharField(_("Item"), max_length=255)
    quantity = models.DecimalField(_("Quantity"), max_digits=64, decimal_places=2)
    price = models.DecimalField(_("Price"), max_digits=64, decimal_places=2)

    class Meta:
        """Meta definition for RequisitionLineItem."""

        verbose_name = _("Requisition Line Item")
        verbose_name_plural = _("Requisition Line Items")
        abstract = False

    def __str__(self):
        """Unicode representation of RequisitionLineItem."""
        return f"{self.item} - #{self.requisition}"

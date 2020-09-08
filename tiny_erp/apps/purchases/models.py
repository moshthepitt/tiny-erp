"""Models module for locations app."""
from typing import Optional

from django.db import models
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext as _

from vega_admin.mixins import TimeStampedModel

from model_reviews.models import AbstractReview

from tiny_erp.abstract_models import TimeStampedAbstractLineItem
from tiny_erp.apps.locations.models import Business, Department, Location
from tiny_erp.apps.products.models import Product
from tiny_erp.constants import EMAIL_TEMPLATE_PATH


# pylint: disable=no-member
class Requisition(TimeStampedModel, AbstractReview):
    """Model definition for Requisition."""

    staff = models.ForeignKey(
        "small_small_hr.StaffProfile",
        verbose_name=_("Staff Member"),
        on_delete=models.PROTECT,
    )
    title = models.CharField(_("Title"), max_length=255)
    business = models.ForeignKey(
        Business, verbose_name=_("Business"), on_delete=models.PROTECT
    )
    location = models.ForeignKey(
        Location, verbose_name=_("Location"), on_delete=models.PROTECT
    )
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.PROTECT
    )
    review_reason = models.TextField(_("Reason"), blank=False, default="")
    review_status = models.CharField(
        _("Status"),
        max_length=1,
        choices=AbstractReview.STATUS_CHOICES,
        default=AbstractReview.PENDING,
        blank=True,
        db_index=True,
    )
    date_placed = models.DateField(_("Date Placed"))
    date_required = models.DateField(_("Date Required"))
    total = models.DecimalField(
        _("Total"), max_digits=64, decimal_places=2, blank=True, default=0
    )

    # MODEL REVIEW OPTIONS
    email_template_path = EMAIL_TEMPLATE_PATH
    # path to function that will be used to determine reviewers
    set_reviewers_function: Optional[
        str
    ] = "tiny_erp.apps.purchases.reviews.set_requisition_reviewer"
    # path to function that will be used to send email to reviewers
    request_for_review_function: Optional[
        str
    ] = "tiny_erp.apps.purchases.emails.send_requisition_filed_email"
    # path to function that will be used to send email to user after review
    review_complete_notify_function: Optional[
        str
    ] = "tiny_erp.apps.purchases.emails.send_requisition_approved_email"

    class Meta:
        """Meta definition for Requisition."""

        abstract = False
        verbose_name = _("Requisition")
        verbose_name_plural = _("Requisitions")

    def get_total(self):
        """Get the total amount."""
        agg = RequisitionLineItem.objects.filter(requisition=self).aggregate(
            total=Coalesce(
                models.Sum(models.F("internal_price") * models.F("quantity")),
                models.Value(0),
            )
        )
        return agg["total"]

    def set_total(self):
        """Save the total to the DB."""
        self.total = self.get_total()
        self.save()

    def __str__(self):
        """Unicode representation of Requisition."""
        return f"#{self.id} {self.title}"


class RequisitionLineItem(TimeStampedAbstractLineItem):
    """Model definition for RequisitionLineItem."""

    requisition = models.ForeignKey(
        Requisition, verbose_name=_("Requisition"), on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        null=True,
        default=None,
        blank=True,
        on_delete=models.SET_NULL,
    )
    item = models.TextField(_("Item"))

    # remove fields from base model class
    name = None

    class Meta:
        """Meta definition for RequisitionLineItem."""

        verbose_name = _("Requisition Line Item")
        verbose_name_plural = _("Requisition Line Items")
        abstract = False

    def __str__(self):
        """Unicode representation of RequisitionLineItem."""
        return f"{self.item} - #{self.requisition}"

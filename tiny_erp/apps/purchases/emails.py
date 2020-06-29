""" tiny-erp purchases app email module"""
from django.conf import settings
from django.utils.translation import ugettext as _

from model_reviews.emails import send_email

from tiny_erp.apps.purchases.models import Requisition


def requisition_filed_email(  # pylint: disable=bad-continuation
    requisition_obj: Requisition,
    template: str = "generic",
    template_path: str = "tiny_erp/email",
):
    """
    Sends an email to admins when a purchase requisition is filed
    """
    msg = getattr(
        settings,
        "TINY_ERP_REQUISITION_FILED_EMAIL_TXT",
        _(
            "There has been a new purchase requisition.  Please log in to process "
            "it."
        ),
    )
    subj = getattr(
        settings, "TINY_ERP_REQUISITION_FILED_EMAIL_SUBJ", _("New Purchase Requisition")
    )
    subj = subj + f" - #{requisition_obj.id}"
    admin_emails = settings.TINY_ERP_ADMIN_EMAILS

    for admin_email in admin_emails:
        send_email(
            name=settings.TINY_ERP_ADMIN_NAME,
            email=admin_email,
            subject=subj,
            message=msg,
            obj=requisition_obj,
            template=template,
            template_path=template_path,
        )


def requisition_updated_email(  # pylint: disable=bad-continuation
    requisition_obj: Requisition,
    template: str = "generic",
    template_path: str = "tiny_erp/email",
):
    """
    Sends an email to admins when a purchase requisition is updated
    """
    staff = requisition_obj.staff
    if staff.user.email:
        msg = getattr(
            settings,
            "TINY_ERP_REQUISITION_UPDATED_EMAIL_TXT",
            _("Your purchase requisition has been updated.  Please log in to view it."),
        )
        subj = getattr(
            settings,
            "TINY_ERP_REQUISITION_UPDATED_EMAIL_SUBJ",
            _("Purchase Requisition Updated"),
        )
        subj = subj + f" - #{requisition_obj.id}"

        send_email(
            name=staff.get_name(),
            email=staff.user.email,
            subject=subj,
            message=msg,
            obj=requisition_obj,
            template=template,
            template_path=template_path,
        )


def requisition_approved_email(  # pylint: disable=bad-continuation
    requisition_obj: Requisition,
    template: str = "generic",
    template_path: str = "tiny_erp/email",
):
    """
    Sends an email to admins when a purchase requisition is approved
    """
    msg = getattr(
        settings,
        "TINY_ERP_REQUISITION_APPROVED_EMAIL_TXT",
        _("The purchase requisition has been approved.  Please log in to view it."),
    )
    subj = getattr(
        settings,
        "TINY_ERP_REQUISITION_APPROVED_EMAIL_SUBJ",
        _("Purchase Requisition Approved"),
    )
    subj = subj + f" - #{requisition_obj.id}"
    accounts_emails = settings.TINY_ERP_ACCOUNTS_EMAILS

    for accounts_email in accounts_emails:
        send_email(
            name=settings.TINY_ERP_ADMIN_NAME,
            email=accounts_email,
            subject=subj,
            message=msg,
            obj=requisition_obj,
            template=template,
            template_path=template_path,
        )

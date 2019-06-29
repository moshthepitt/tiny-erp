""" tiny-erp purchases app email module"""
from django.conf import settings
from django.utils.translation import ugettext as _

from small_small_hr.emails import send_email

from tiny_erp.apps.purchases.models import Requisition


def requisition_filed_email(requisition_obj: Requisition):
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
    admin_emails = settings.TINY_ERP_ADMIN_EMAILS

    for admin_email in admin_emails:
        send_email(
            name=settings.TINY_ERP_ADMIN_NAME,
            email=admin_email,
            subject=subj,
            message=msg,
            obj=requisition_obj,
            template="generic",
            template_path="tiny_erp/email",
        )

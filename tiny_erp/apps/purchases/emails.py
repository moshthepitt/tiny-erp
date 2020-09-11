"""tiny-erp purchases app email module."""
from django.conf import settings
from django.utils.translation import ugettext as _

from model_reviews.emails import get_display_name, send_email
from model_reviews.models import ModelReview, Reviewer

from tiny_erp.apps.purchases.models import Requisition
from tiny_erp.constants import (
    REQUISITION_COMPLETED_EMAIL_TEMPLATE,
    REQUISITION_FILED_EMAIL_TEMPLATE,
)


def requisition_filed_email(  # pylint: disable=bad-continuation
    requisition_obj: Requisition,
    template: str = "generic",
    template_path: str = "tiny_erp/email",
):
    """Send an email to admins when a purchase requisition is filed."""
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


def send_requisition_filed_email(reviewer: Reviewer):
    """Send email when a purchase requisition is filed."""
    if reviewer.user.email:
        source = reviewer.review.content_object
        send_email(
            name=get_display_name(reviewer.user),
            email=reviewer.user.email,
            subject=source.review_request_email_subject,
            message=source.review_request_email_body,
            obj=reviewer.review,
            cc_list=None,
            template=REQUISITION_FILED_EMAIL_TEMPLATE,
            template_path=source.email_template_path,
        )


def requisition_updated_email(  # pylint: disable=bad-continuation
    requisition_obj: Requisition,
    template: str = "generic",
    template_path: str = "tiny_erp/email",
):
    """Send an email to admins when a purchase requisition is updated."""
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
    """Send an email to admins when a purchase requisition is approved."""
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


def send_requisition_approved_email(review_obj: ModelReview):
    """Send notice that purchase requisition is approved.."""
    if not review_obj.needs_review() and review_obj.user:
        if review_obj.user.email:
            source = review_obj.content_object
            send_email(
                name=get_display_name(review_obj.user),
                email=review_obj.user.email,
                subject=source.review_complete_email_subject,
                message=source.review_complete_email_body,
                obj=review_obj,
                cc_list=None,
                template=REQUISITION_COMPLETED_EMAIL_TEMPLATE,
                template_path=source.email_template_path,
            )

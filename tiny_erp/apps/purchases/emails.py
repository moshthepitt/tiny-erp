"""tiny-erp purchases app email module."""
from model_reviews.emails import get_display_name, send_email
from model_reviews.models import ModelReview, Reviewer

from tiny_erp.constants import (
    REQUISITION_COMPLETED_EMAIL_TEMPLATE,
    REQUISITION_FILED_EMAIL_TEMPLATE,
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

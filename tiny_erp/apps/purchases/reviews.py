"""Reviews module."""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Min

from model_reviews.models import Reviewer

from tiny_erp.apps.purchases.emails import send_requisition_filed_email


def set_reviewer_by_email(email: str, review_obj: models.Model, level: int = 0):
    """Set reviewer using email address."""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        pass
    else:
        # pylint: disable=bad-continuation
        if not Reviewer.objects.filter(
            review=review_obj, user=user, level=level
        ).exists():
            reviewer = Reviewer(review=review_obj, user=user, level=level)
            reviewer.save()  # ensure save method is called


def set_requisition_reviewer(review_obj: models.Model):
    """
    Set reviewer for purchase requisitions.

    If TINY_ERP_REQUISITION_REVIEWS_TIERS is false then every level = 0
    otherwise reviewer levels correspond to their indices on the reviewer_emails array
    """
    reviewer_emails = settings.TINY_ERP_REQUISITION_REVIEWERS
    if reviewer_emails:
        use_tiers = settings.TINY_ERP_REQUISITION_REVIEWS_TIERS
        for idx, reviewer_email in enumerate(reviewer_emails):
            level = 0
            if use_tiers:
                level = idx
            set_reviewer_by_email(
                email=reviewer_email, review_obj=review_obj, level=level
            )


def initial_request_for_review_function(reviewer: Reviewer):
    """
    Send the initial request(s) for review.

    This function is called when a Reviewer object is created (not updated).
    """
    if settings.TINY_ERP_REQUISITION_REVIEWS_TIERS:
        # check if this reviewer is the lowest level and then send the email
        min_lvl = Reviewer.objects.filter(review=reviewer.review).aggregate(
            min_lvl=Min("level")
        )["min_lvl"]
        if reviewer.level == min_lvl:
            send_requisition_filed_email(reviewer=reviewer)
    else:
        # proceed as normal
        send_requisition_filed_email(reviewer=reviewer)


def notify_next_reviewers(review_obj: models.Model):
    """Get next level reviewers and notify them."""
    next_lvl = Reviewer.objects.filter(reviewed=False, review=review_obj).aggregate(
        next_lvl=Min("level")
    )["next_lvl"]
    for reviewer in Reviewer.objects.filter(reviewed=False, level=next_lvl):
        send_requisition_filed_email(reviewer=reviewer)


def set_requisition_review_user(review_obj: models.Model):
    """Set user for review model object."""
    if not review_obj.user:
        requisition = review_obj.content_object
        review_obj.user = requisition.staff.user

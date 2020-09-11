"""Reviews module."""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from model_reviews.models import Reviewer


def set_reviewer_by_email(email: str, review_obj: models.Model, level: int = 0):
    """Set reviewer using email address."""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        pass
    else:
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

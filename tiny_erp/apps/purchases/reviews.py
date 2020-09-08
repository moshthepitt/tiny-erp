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
    """Set reviewer for purchase requisitions."""
    reviewer_emails = settings.TINY_ERP_REQUISITION_REVIEWERS
    if reviewer_emails:
        use_tiers = settings.TINY_ERP_REQUISITION_REVIEWS_TIERS
        if use_tiers:
            # set the first person as the reviewer
            set_reviewer_by_email(reviewer_emails[0], review_obj)
        else:
            for idx, reviewer_email in enumerate(reviewer_emails):
                set_reviewer_by_email(reviewer_email, review_obj, idx)


# def set_next_reviewer(review_obj: models.Model):
#     """Set the next reviewer."""
#     reviewer_emails = settings.TINY_ERP_REQUISITION_REVIEWERS
#     use_tiers = settings.TINY_ERP_REQUISITION_REVIEWS_TIERS
#     if reviewer_emails and use_tiers:
#         # first lets get all the reviewers who have already reviewed
#         Reviewer.objects.filter(review=review_obj, )

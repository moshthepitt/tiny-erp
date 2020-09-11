"""Test reviews stuff."""
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.test import override_settings

from model_bakery import baker
from model_reviews.models import ModelReview, Reviewer

from tiny_erp.apps.purchases.reviews import set_requisition_reviewer

from .base import TestBase


class TestReviews(TestBase):
    """Test reviews stuff."""

    @override_settings(
        TINY_ERP_REQUISITION_REVIEWS_TIERS=True,
        TINY_ERP_REQUISITION_REVIEWERS=[
            "1@example.com",
            "2@example.com",
            "3@example.com",
        ],
    )
    @patch("tiny_erp.apps.purchases.reviews.send_requisition_filed_email")
    def test_set_requisition_reviewer(self, mock):
        """Test set_requisition_reviewer."""
        obj = baker.make(
            "purchases.Requisition",
            staff=self.staffprofile,
            location=self.location,
            business=self.business,
            department=self.department,
            date_placed="2019-01-01",
            date_required="2019-02-02",
            review_reason="Science, bitch",
        )

        user = baker.make("auth.User", username="mosh")
        reviewer1 = baker.make(
            "auth.User", username="1@example.com", email="1@example.com"
        )
        reviewer2 = baker.make(
            "auth.User", username="2@example.com", email="2@example.com"
        )
        reviewer3 = baker.make(
            "auth.User", username="3@example.com", email="3@example.com"
        )
        obj_type = ContentType.objects.get_for_model(obj)

        # create without sending signals
        ModelReview.objects.bulk_create(
            [ModelReview(user=user, content_type=obj_type, object_id=obj.id)]
        )
        review = ModelReview.objects.get(
            user=user, content_type=obj_type, object_id=obj.id
        )

        set_requisition_reviewer(review)

        for idx, item in enumerate([reviewer1, reviewer2, reviewer3]):
            self.assertTrue(
                Reviewer.objects.filter(user=item, review=review, level=idx,).exists()
            )

        mock.assert_called_once_with(
            reviewer=Reviewer.objects.get(user=reviewer1, review=review, level=0,)
        )

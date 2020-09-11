"""Test reviews stuff."""
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, override_settings

from model_bakery import baker
from model_reviews.forms import PerformReview
from model_reviews.models import ModelReview, Reviewer

from .base import TestBase


class TestReviews(TestBase):
    """Test reviews stuff."""

    def setUp(self):
        """Set up test class."""
        super().setUp()
        self.factory = RequestFactory()

    @override_settings(
        TINY_ERP_REQUISITION_REVIEWS_TIERS=True,
        TINY_ERP_REQUISITION_REVIEWERS=[
            "1@example.com",
            "2@example.com",
            "3@example.com",
        ],
    )
    @patch("tiny_erp.apps.purchases.reviews.send_requisition_filed_email")
    def test_tiered_reviewers(self, mock):
        """Test that tiered reviewers work as expected."""
        reviewer1 = baker.make(
            "auth.User", username="1@example.com", email="1@example.com"
        )
        reviewer2 = baker.make(
            "auth.User", username="2@example.com", email="2@example.com"
        )
        reviewer3 = baker.make(
            "auth.User", username="3@example.com", email="3@example.com"
        )

        # creating this object calls set_requisition_reviewer via a signal
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

        obj_type = ContentType.objects.get_for_model(obj)

        review = ModelReview.objects.get(content_type=obj_type, object_id=obj.id)

        # test that set_requisition_reviewer resulted in 3 reviewers
        for idx, item in enumerate([reviewer1, reviewer2, reviewer3]):
            self.assertTrue(
                Reviewer.objects.filter(user=item, review=review, level=idx,).exists()
            )
        # test that set_requisition_reviewer resulted in only first reviewer getting email
        mock.assert_called_once_with(
            reviewer=Reviewer.objects.get(user=reviewer1, review=review, level=0,)
        )

        # let reviewer1 approve it
        request = self.factory.get("/")
        request.session = {}
        request.user = reviewer1

        data = {
            "review": review.pk,
            "reviewer": Reviewer.objects.get(user=reviewer1, review=review).pk,
            "review_status": ModelReview.APPROVED,
        }

        form = PerformReview(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        review.refresh_from_db()
        self.assertEqual(ModelReview.PENDING, review.review_status)

        # test that reviewer2 got email to go and review
        self.assertEqual(2, mock.call_count)
        mock.assert_called_with(
            reviewer=Reviewer.objects.get(user=reviewer2, review=review, level=1,)
        )

        # let reviewer2 approve it
        request = self.factory.get("/")
        request.session = {}
        request.user = reviewer1

        data = {
            "review": review.pk,
            "reviewer": Reviewer.objects.get(user=reviewer2, review=review).pk,
            "review_status": ModelReview.APPROVED,
        }

        form = PerformReview(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        review.refresh_from_db()
        self.assertEqual(ModelReview.PENDING, review.review_status)

        # test that reviewer3 got email to go and review
        self.assertEqual(3, mock.call_count)
        mock.assert_called_with(
            reviewer=Reviewer.objects.get(user=reviewer3, review=review, level=2,)
        )

        # let reviewer3 approve it
        request = self.factory.get("/")
        request.session = {}
        request.user = reviewer1

        data = {
            "review": review.pk,
            "reviewer": Reviewer.objects.get(user=reviewer3, review=review).pk,
            "review_status": ModelReview.APPROVED,
        }

        form = PerformReview(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        # test that another request to review email was not sent
        self.assertEqual(3, mock.call_count)

        review.refresh_from_db()
        self.assertEqual(ModelReview.APPROVED, review.review_status)

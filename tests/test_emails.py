"""Module to test tiny_erp Emails."""
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.test import override_settings

from model_bakery import baker
from model_reviews.forms import PerformReview
from model_reviews.models import ModelReview, Reviewer

from tiny_erp.apps.purchases.emails import (
    send_requisition_completed_email,
    send_requisition_filed_email,
)

from .base import TestBase


@override_settings(  # pylint: disable=too-many-ancestors
    # TINY_ERP_ADMIN_EMAILS=["erp@example.com"],
    # TINY_ERP_ACCOUNTS_EMAILS=["accounts@example.com"],
    # TINY_ERP_ADMIN_NAME="mosh",
    TINY_ERP_REQUISITION_REVIEWS_TIERS=True,
    TINY_ERP_REQUISITION_REVIEWERS=["erp@example.com"],
)
class TestEmails(TestBase):
    """Test class for emails."""

    maxDiff = None

    def setUp(self):
        """Set up test class."""
        super().setUp()
        self.reviewer1 = baker.make(
            "auth.User",
            username="webmaster",
            email="erp@example.com",
            first_name="mosh",
            last_name="",
        )

    def test_requisition_filed_email(self):
        """Test requisition_filed_email."""
        requisition = baker.make(
            "purchases.Requisition",
            title="New supplies",
            staff=self.staffprofile,
            location=self.location,
            business=self.business,
            department=self.department,
            date_placed="2019-01-01",
            date_required="2019-02-02",
            review_reason="Science, bitch",
        )

        obj_type = ContentType.objects.get_for_model(requisition)
        review = ModelReview.objects.get(
            content_type=obj_type, object_id=requisition.id
        )
        reviewer = Reviewer.objects.get(user=self.reviewer1, review=review)

        with patch("tiny_erp.apps.purchases.emails.send_email") as mock:
            send_requisition_filed_email(reviewer)
            mock.assert_called_with(
                name="mosh",
                email="erp@example.com",
                subject="New Purchase Requisition",
                message=(
                    "There has been a new purchase requisition.  Please log in to process it."  # pylint: disable=line-too-long  # noqa
                ),
                obj=review,
                cc_list=None,
                template="requisition_filed",
                template_path="tiny_erp/email",
            )

        #     send_requisition_filed_email(review)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(
            f"Purchase Requisition - #{requisition.id}: {requisition.title}",
            mail.outbox[0].subject,
        )
        self.assertEqual(["mosh <erp@example.com>"], mail.outbox[0].to)
        self.assertMatchSnapshot(mail.outbox[0].body)
        self.assertMatchSnapshot(mail.outbox[0].alternatives[0][0])

    def test_requisition_completed_email(self):
        """Test requisition_completed_email."""
        requisition = baker.make(  # this sends an email
            "purchases.Requisition",
            title="Newer supplies",
            staff=self.staffprofile,
            location=self.location,
            business=self.business,
            department=self.department,
            date_placed="2019-04-03",
            date_required="2019-04-10",
            review_reason="Science, bitch",
        )
        obj_type = ContentType.objects.get_for_model(requisition)
        review = ModelReview.objects.get(
            content_type=obj_type, object_id=requisition.id
        )

        # approve it
        data = {
            "review": review.pk,
            "reviewer": Reviewer.objects.get(user=self.reviewer1, review=review).pk,
            "review_status": ModelReview.APPROVED,
        }
        form = PerformReview(data=data)
        self.assertTrue(form.is_valid())
        form.save()  # this sends an email
        review.refresh_from_db()
        self.assertEqual(ModelReview.APPROVED, review.review_status)

        with patch("tiny_erp.apps.purchases.emails.send_email") as mock:
            send_requisition_completed_email(review)
            mock.assert_called_with(
                name="Bob Ndoe",
                email="bob@example.com",
                subject="Purchase Requisition Processed",
                message="The purchase requisition has been processed.  Please log in to view it.",  # noqa  pylint: disable=line-too-long
                obj=review,
                template="requisition_completed",
                template_path="tiny_erp/email",
                cc_list=None,
            )

        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(
            f'Your purchase requisition #{requisition.id}: "{requisition.title}" has been approved',  # noqa  pylint: disable=line-too-long
            mail.outbox[1].subject,
        )
        self.assertEqual(["Bob Ndoe <bob@example.com>"], mail.outbox[1].to)
        self.assertMatchSnapshot(mail.outbox[1].body)
        self.assertMatchSnapshot(mail.outbox[1].alternatives[0][0])

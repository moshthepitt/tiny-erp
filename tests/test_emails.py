"""Module to test tiny_erp Emails."""
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.test import override_settings

from model_bakery import baker
from model_reviews.models import ModelReview, Reviewer

from tiny_erp.apps.purchases.emails import (
    send_requisition_approved_email,
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
        """
        Test requisition_filed_email
        """
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

    def test_requisition_approved_email(self):
        """
        Test requisition_approved_email
        """
        requisition = baker.make(
            "purchases.Requisition",
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

        with patch("tiny_erp.apps.purchases.emails.send_email") as mock:
            send_requisition_approved_email(review)
            mock.assert_called_with(
                name="mosh",
                email="accounts@example.com",
                subject=f"Purchase Requisition Approved - #{requisition.id}",
                message="The purchase requisition has been approved.  Please log in to view it.",  # noqa  pylint: disable=line-too-long
                obj=requisition,
                template="generic",
                template_path="tiny_erp/email",
            )

        send_requisition_approved_email(review)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(
            f"Purchase Requisition Approved - #{requisition.id}", mail.outbox[0].subject
        )
        self.assertEqual(["mosh <accounts@example.com>"], mail.outbox[0].to)
        self.assertEqual(
            "Hello,\n\nThe purchase requisition has been approved.  Please "
            "log in to view it.\n\nThank you,\n\n"
            "example.com\n------\nhttp://example.com\n",
            mail.outbox[0].body,
        )
        self.assertEqual(
            "Hello,<br/><br/><p>The purchase requisition has been approved."
            "  Please log in to view it.</p><br/><br/>"
            "Thank you,<br/>example.com<br/>------<br/>http://example.com",
            mail.outbox[0].alternatives[0][0],
        )

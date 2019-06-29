"""
Module to test tiny_erp Emails
"""
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings

from model_mommy import mommy

from tiny_erp.apps.purchases.emails import (
    requisition_filed_email,
    requisition_updated_email,
)


@override_settings(
    TINY_ERP_ADMIN_EMAILS=["erp@example.com"],
    TINY_ERP_ACCOUNTS_EMAILS=["accounts@example.com"],
    TINY_ERP_ADMIN_NAME="mosh",
)
class TestEmails(TestCase):
    """
    Test class for emails
    """

    def setUp(self):
        """
        Set up
        """
        self.user = mommy.make(
            "auth.User", first_name="Bob", last_name="Ndoe", email="bob@example.com"
        )
        self.staffprofile = mommy.make("small_small_hr.StaffProfile", user=self.user)
        self.business = mommy.make("locations.Business", name="X Inc")
        self.location = mommy.make("locations.Location", name="Voi")
        self.department = mommy.make("locations.Department", name="Science")

    def test_requisition_filed_email(self):
        """
        Test requisition_filed_email
        """
        requisition = mommy.make(
            "purchases.Requisition",
            staff=self.staffprofile,
            location=self.location,
            business=self.business,
            department=self.department,
            date_placed="2019-01-01",
            date_required="2019-02-02",
            reason="Science, bitch",
        )

        with patch("tiny_erp.apps.purchases.emails.send_email") as mock:
            requisition_filed_email(requisition)
            mock.assert_called_with(
                name="mosh",
                email="erp@example.com",
                subject=f"New Purchase Requisition - #{requisition.id}",
                message="There has been a new purchase requisition.  Please log in to process it.",  # noqa  pylint: disable=line-too-long
                obj=requisition,
                template="generic",
                template_path="tiny_erp/email",
            )

        requisition_filed_email(requisition)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(
            f"New Purchase Requisition - #{requisition.id}", mail.outbox[0].subject
        )
        self.assertEqual(["mosh <erp@example.com>"], mail.outbox[0].to)
        self.assertEqual(
            "Hello,\n\nThere has been a new purchase requisition.  Please "
            "log in to process it.\n\nThank you,\n\n"
            "example.com\n------\nhttp://example.com\n",
            mail.outbox[0].body,
        )
        self.assertEqual(
            "Hello,<br/><br/><p>There has been a new purchase "
            "requisition.  Please log in to process it.</p><br/><br/>"
            "Thank you,<br/>example.com<br/>------<br/>http://example.com",
            mail.outbox[0].alternatives[0][0],
        )

    def test_requisition_updated_email(self):
        """
        Test requisition_updated_email
        """
        requisition = mommy.make(
            "purchases.Requisition",
            staff=self.staffprofile,
            location=self.location,
            business=self.business,
            department=self.department,
            date_placed="2019-03-03",
            date_required="2019-03-10",
            reason="Science, bitch",
        )

        with patch("tiny_erp.apps.purchases.emails.send_email") as mock:
            requisition_updated_email(requisition)
            mock.assert_called_with(
                name="Bob Ndoe",
                email="bob@example.com",
                subject=f"Purchase Requisition Updated - #{requisition.id}",
                message="Your purchase requisition has been updated.  Please log in to view it.",  # noqa  pylint: disable=line-too-long
                obj=requisition,
                template="generic",
                template_path="tiny_erp/email",
            )

        requisition_updated_email(requisition)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(
            f"Purchase Requisition Updated - #{requisition.id}", mail.outbox[0].subject
        )
        self.assertEqual(["Bob Ndoe <bob@example.com>"], mail.outbox[0].to)
        self.assertEqual(
            "Hello,\n\nYour purchase requisition has been updated.  Please "
            "log in to view it.\n\nThank you,\n\n"
            "example.com\n------\nhttp://example.com\n",
            mail.outbox[0].body,
        )
        self.assertEqual(
            "Hello,<br/><br/><p>Your purchase requisition has been updated."
            "  Please log in to view it.</p><br/><br/>"
            "Thank you,<br/>example.com<br/>------<br/>http://example.com",
            mail.outbox[0].alternatives[0][0],
        )

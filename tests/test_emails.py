"""
Module to test tiny_erp Emails
"""
from unittest.mock import patch

from django.test import TestCase, override_settings

from model_mommy import mommy

from tiny_erp.apps.purchases.emails import requisition_filed_email


@override_settings(
    TINY_ERP_ADMIN_EMAILS=["erp@example.com"], TINY_ERP_ADMIN_NAME="mosh"
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

    @patch("tiny_erp.apps.purchases.emails.send_email")
    def test_requisition_filed_email(self, mock):
        """
        Test requisition_filed_email
        """
        business = mommy.make("locations.Business", name="X Inc")
        location = mommy.make("locations.Location", name="Voi")
        department = mommy.make("locations.Department", name="Science")

        requisition = mommy.make(
            "purchases.Requisition",
            staff=self.staffprofile,
            location=location,
            business=business,
            department=department,
            date_placed="2019-01-01",
            date_required="2019-02-02",
            reason="Science, bitch",
        )

        requisition_filed_email(requisition)

        mock.assert_called_with(
            name="mosh",
            email="erp@example.com",
            subject="New Purchase Requisition",
            message="There has been a new purchase requisition.  Please log in to process it.",  # noqa  pylint: disable=line-too-long
            obj=requisition,
            template="generic",
            template_path="tiny_erp/email",
        )

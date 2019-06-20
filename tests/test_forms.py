"""module to test tiny-erp forms"""
from datetime import date

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from model_mommy import mommy

from tiny_erp.apps.purchases.forms import RequisitionForm


class TestForms(TestCase):
    """
    Test class for forms
    """

    def setUp(self):
        """
        Setup test class
        """
        self.factory = RequestFactory()

    def test_role_form(self):
        """
        Test RoleForm
        """
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        user = mommy.make("auth.User", first_name="Bob", last_name="Ndoe")
        staffprofile = mommy.make("small_small_hr.StaffProfile", user=user)
        business = mommy.make("locations.Business", name="X Inc")
        location = mommy.make("locations.Location", name="Voi")
        department = mommy.make("locations.Department", name="Science")

        data = {
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "reason": "Science, bitch",
        }

        form = RequisitionForm(data=data)
        self.assertTrue(form.is_valid())
        requisition = form.save()
        self.assertEqual(staffprofile, requisition.staff)
        self.assertEqual(location, requisition.location)
        self.assertEqual(business, requisition.business)
        self.assertEqual(department, requisition.department)
        self.assertEqual(date(2019, 1, 1), requisition.date_placed)
        self.assertEqual(date(2019, 2, 2), requisition.date_required)
        self.assertEqual("Science, bitch", requisition.reason)

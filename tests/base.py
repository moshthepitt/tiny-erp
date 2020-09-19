"""Base test module."""
from model_bakery import baker
from snapshottest.django import TestCase


class TestBase(TestCase):
    """Base test class."""

    def setUp(self):
        """Set up."""
        super().setUp()
        self.user = baker.make(
            "auth.User", first_name="Bob", last_name="Ndoe", email="bob@example.com"
        )
        self.staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        self.business = baker.make("locations.Business", name="X Inc")
        self.location = baker.make("locations.Location", name="Voi")
        self.department = baker.make("locations.Department", name="Science")

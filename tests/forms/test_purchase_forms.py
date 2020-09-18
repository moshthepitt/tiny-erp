"""module to test tiny-erp forms."""
from datetime import date
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.forms.models import inlineformset_factory
from django.test import RequestFactory, override_settings
from django.urls import reverse

from small_small_hr.models import StaffProfile

from crispy_forms.utils import render_crispy_form
from model_bakery import baker
from model_reviews.models import ModelReview
from prices import Money
from snapshottest.django import TestCase

from tiny_erp.apps.locations.models import Business, Department, Location
from tiny_erp.apps.purchases.forms import (
    RequisitionForm,
    RequisitionLineItemForm,
    RequisitionLineItemProductForm,
    RequisitionProductForm,
    UpdatedRequisitionProductForm,
    UpdateRequisitionForm,
)
from tiny_erp.apps.purchases.models import Requisition, RequisitionLineItem


def make_staffprofile(attrs: dict):
    """
    Make StaffProfile object.

    This is necessary because:
        - model_bakery isn't working well for StaffProfile
        - we need to set lft and rght
    """
    staff = StaffProfile(**attrs, lft=None, rght=None,)
    staff.save()
    return staff


@override_settings(
    TINY_ERP_REQUISITION_REVIEWS_TIERS=True,
    TINY_ERP_REQUISITION_REVIEWERS=["webmaster@localhost"],
)
class TestForms(TestCase):
    """Test class for forms."""

    maxDiff = None

    def setUp(self):
        """Set up test class."""
        self.factory = RequestFactory()
        Business.objects.all().delete()
        Department.objects.all().delete()
        Location.objects.all().delete()
        self.user = baker.make("auth.User", first_name="Bob", last_name="Ndoe")
        self.reviewer1 = baker.make(
            "auth.User",
            username="webmaster",
            email="webmaster@localhost",
            first_name="Web",
            last_name="Master",
        )

    @patch("tiny_erp.apps.purchases.emails.send_email")
    def test_requisition_form(self, email_mock):
        """Test RequisitionForm."""
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        baker.make("small_small_hr.StaffProfile", _quantity=2)
        business = baker.make("locations.Business", name="X Inc")
        location = baker.make("locations.Location", name="Voi")
        department = baker.make("locations.Department", name="Science")

        data = {
            "title": "Cheers Baba",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "Science, bitch",
        }

        form = RequisitionForm(data=data)
        self.assertTrue(form.is_valid())
        requisition = form.save()
        self.assertEqual("Cheers Baba", requisition.title)
        self.assertEqual(staffprofile, requisition.staff)
        self.assertEqual(location, requisition.location)
        self.assertEqual(business, requisition.business)
        self.assertEqual(department, requisition.department)
        self.assertEqual(date(2019, 1, 1), requisition.date_placed)
        self.assertEqual(date(2019, 2, 2), requisition.date_required)
        self.assertEqual("Science, bitch", requisition.review_reason)

        # check that a ModelReview object is created
        obj_type = ContentType.objects.get_for_model(requisition)
        self.assertEqual(
            1,
            ModelReview.objects.filter(
                content_type=obj_type, object_id=requisition.id
            ).count(),
        )
        review = ModelReview.objects.get(
            content_type=obj_type, object_id=requisition.id
        )
        self.assertTrue(Requisition.PENDING, review.review_status)

        self.assertEqual(1, email_mock.call_count)

        email_mock.assert_called_once_with(
            name="Web Master",
            email="webmaster@localhost",
            subject="New Purchase Requisition",
            message=(
                "There has been a new purchase requisition.  Please log in to process it."
            ),
            obj=review,
            cc_list=None,
            template="requisition_filed",
            template_path="tiny_erp/email",
        )

    @patch("tiny_erp.apps.purchases.emails.send_email")
    def test_requisition_product_form(self, email_mock):
        """Test RequisitionProductForm."""
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        baker.make("small_small_hr.StaffProfile", _quantity=2)
        business = baker.make("locations.Business", name="X Inc")
        location = baker.make("locations.Location", name="Voi")
        department = baker.make("locations.Department", name="Science")

        data = {
            "title": "Cheers Baba",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "Science, bitch",
        }

        form = RequisitionProductForm(data=data)
        self.assertTrue(form.is_valid())
        requisition = form.save()
        self.assertEqual("Cheers Baba", requisition.title)
        self.assertEqual(staffprofile, requisition.staff)
        self.assertEqual(location, requisition.location)
        self.assertEqual(business, requisition.business)
        self.assertEqual(department, requisition.department)
        self.assertEqual(date(2019, 1, 1), requisition.date_placed)
        self.assertEqual(date(2019, 2, 2), requisition.date_required)
        self.assertEqual("Science, bitch", requisition.review_reason)

        self.assertEqual(1, email_mock.call_count)

    @patch("tiny_erp.apps.purchases.emails.send_email")
    def test_updated_requisition_form(self, email_mock):
        """Test UpdateRequisitionForm."""
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        baker.make("small_small_hr.StaffProfile", _quantity=2)
        business = baker.make("locations.Business", name="X Inc")
        location = baker.make("locations.Location", name="Voi")
        department = baker.make("locations.Department", name="Science")
        requisition = baker.make(
            "purchases.Requisition",
            title="Cheers Baba",
            staff=staffprofile,
            location=location,
            department=department,
            business=business,
            date_placed="2019-06-24",
            date_required="2019-06-24",
            id=99,
        )

        data = {
            "title": "Subaru Supplies",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "changed this",
        }
        form = UpdateRequisitionForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Subaru Supplies", requisition.title)
        self.assertEqual("changed this", requisition.review_reason)
        self.assertEqual(1, email_mock.call_count)

        data = {
            "title": "Shhh... Housekeeping!",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "Not good",
        }
        form = UpdateRequisitionForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Shhh... Housekeeping!", requisition.title)
        self.assertEqual("Not good", requisition.review_reason)
        self.assertEqual(1, email_mock.call_count)

        data = {
            "title": "Cheers Baba",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "Great",
        }
        form = UpdateRequisitionForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Cheers Baba", requisition.title)
        self.assertEqual("Great", requisition.review_reason)
        self.assertEqual(1, email_mock.call_count)

    @patch("tiny_erp.apps.purchases.emails.send_email")
    def test_updated_requisition_product_form(  # pylint: disable=bad-continuation
        self, email_mock
    ):
        """Test UpdatedRequisitionProductForm."""
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        baker.make("small_small_hr.StaffProfile", _quantity=2)
        business = baker.make("locations.Business", name="X Inc")
        location = baker.make("locations.Location", name="Voi")
        department = baker.make("locations.Department", name="Science")
        requisition = baker.make(
            "purchases.Requisition",
            title="Cheers Baba",
            staff=staffprofile,
            location=location,
            department=department,
            business=business,
            date_placed="2019-06-24",
            date_required="2019-06-24",
            id=99,
        )

        data = {
            "title": "Subaru Supplies",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "changed this",
        }
        form = UpdatedRequisitionProductForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Subaru Supplies", requisition.title)
        self.assertEqual("changed this", requisition.review_reason)
        self.assertEqual(1, email_mock.call_count)

        data = {
            "title": "Shhh... Housekeeping!",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "Not good",
        }
        form = UpdatedRequisitionProductForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Shhh... Housekeeping!", requisition.title)
        self.assertEqual("Not good", requisition.review_reason)
        self.assertEqual(1, email_mock.call_count)

        data = {
            "title": "Cheers Baba",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "Great",
        }
        form = UpdatedRequisitionProductForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Cheers Baba", requisition.title)
        self.assertEqual("Great", requisition.review_reason)
        self.assertEqual(1, email_mock.call_count)

    @override_settings(ROOT_URLCONF="tests.crud")
    def test_full_requisition_form(self):
        """Test the full implementation of the requisition form."""
        Requisition.objects.all().delete()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        business = baker.make("locations.Business", name="X Inc")
        location = baker.make("locations.Location", name="Voi")
        department = baker.make("locations.Department", name="Science")
        data = {
            "title": "Kitchen Supplies",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "review_reason": "I love oov",
            "total": 0,
            "requisitionlineitem_set-TOTAL_FORMS": 2,
            "requisitionlineitem_set-INITIAL_FORMS": 0,
            "requisitionlineitem_set-MIN_NUM_FORMS": 0,
            "requisitionlineitem_set-0-item": "Pen",
            "requisitionlineitem_set-0-quantity": 3,
            "requisitionlineitem_set-0-internal_price": 7,
            "requisitionlineitem_set-1-item": "Ink",
            "requisitionlineitem_set-1-quantity": 1,
            "requisitionlineitem_set-1-internal_price": 20,
        }
        url = reverse("purchases.requisition-create")
        res = self.client.post(url, data)
        self.assertEqual(302, res.status_code)
        self.assertRedirects(res, reverse("purchases.requisition-list"))
        self.assertEqual(1, Requisition.objects.all().count())
        requisition = Requisition.objects.first()

        self.assertEqual(
            2, RequisitionLineItem.objects.filter(requisition=requisition).count()
        )
        self.assertEqual(41, requisition.total)
        self.assertEqual(Requisition.PENDING, requisition.review_status)
        self.assertEqual("I love oov", requisition.review_reason)
        self.assertEqual("Kitchen Supplies", requisition.title)

        url = reverse("purchases.requisition-update", kwargs={"pk": requisition.id})
        data = {
            "id": requisition.id,
            "title": "Bar Supplies",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "total": 0,
            "review_reason": "Nice",
            "requisitionlineitem_set-TOTAL_FORMS": 3,
            "requisitionlineitem_set-INITIAL_FORMS": 2,
            "requisitionlineitem_set-MIN_NUM_FORMS": 0,
            "requisitionlineitem_set-MAX_NUM_FORMS": 1000,
            "requisitionlineitem_set-0-id": requisition.requisitionlineitem_set.first().id,  # noqa
            "requisitionlineitem_set-0-item": "Pen",
            "requisitionlineitem_set-0-quantity": 3,
            "requisitionlineitem_set-0-internal_price": 7,
            "requisitionlineitem_set-0-requisition": requisition.id,
            "requisitionlineitem_set-1-id": requisition.requisitionlineitem_set.last().id,
            "requisitionlineitem_set-1-item": "Ink",
            "requisitionlineitem_set-1-quantity": 1,
            "requisitionlineitem_set-1-internal_price": 20,
            "requisitionlineitem_set-1-DELETE": "1",  # this line item is being deleted
            "requisitionlineitem_set-1-requisition": requisition.id,
            "requisitionlineitem_set-2-item": "Pencil",
            "requisitionlineitem_set-2-quantity": 8,
            "requisitionlineitem_set-2-internal_price": 17,
            "requisitionlineitem_set-2-requisition": requisition.id,
        }

        res = self.client.post(url, data)
        requisition.refresh_from_db()
        self.assertEqual(157, requisition.total)
        self.assertEqual("Bar Supplies", requisition.title)
        self.assertEqual("Nice", requisition.review_reason)

    @override_settings(ROOT_URLCONF="tests.crud")
    def test_full_requisition_product_form(self):
        """Test the full implementation of the requisition product form."""
        Requisition.objects.all().delete()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        business = baker.make("locations.Business", name="X Inc")
        location = baker.make("locations.Location", name="Voi")
        department = baker.make("locations.Department", name="Science")
        product1 = baker.make(
            "products.product", name="Juice", sku="778", internal_amount=250
        )
        product2 = baker.make(
            "products.product", name="Water", sku="779", internal_amount=50
        )
        data = {
            "title": "Kitchen Supplies",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/11/2019",
            "date_required": "02/12/2019",
            "review_reason": "I love oov",
            "total": 0,
            "requisitionlineitem_set-TOTAL_FORMS": 1,
            "requisitionlineitem_set-INITIAL_FORMS": 0,
            "requisitionlineitem_set-MIN_NUM_FORMS": 0,
            "requisitionlineitem_set-0-product": product1.pk,
            "requisitionlineitem_set-0-quantity": 3,
            "requisitionlineitem_set-0-internal_price": 1,
        }
        url = reverse("req-products-create")
        res = self.client.post(url, data)
        self.assertEqual(302, res.status_code)
        self.assertRedirects(res, reverse("req-products-list"))
        self.assertEqual(1, Requisition.objects.all().count())
        requisition = Requisition.objects.first()

        self.assertEqual(
            1, RequisitionLineItem.objects.filter(requisition=requisition).count()
        )
        self.assertEqual(750, requisition.total)
        self.assertEqual(Requisition.PENDING, requisition.review_status)
        self.assertEqual("I love oov", requisition.review_reason)
        self.assertEqual("Kitchen Supplies", requisition.title)

        url = reverse("req-products-update", kwargs={"pk": requisition.id})
        data = {
            "id": requisition.id,
            "title": "Bar Supplies",
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "total": 0,
            "review_reason": "Nice",
            "requisitionlineitem_set-TOTAL_FORMS": 2,
            "requisitionlineitem_set-INITIAL_FORMS": 1,
            "requisitionlineitem_set-MIN_NUM_FORMS": 0,
            "requisitionlineitem_set-MAX_NUM_FORMS": 1000,
            "requisitionlineitem_set-0-id": requisition.requisitionlineitem_set.first().id,  # noqa
            "requisitionlineitem_set-0-product": product1.pk,
            "requisitionlineitem_set-0-quantity": 3,
            "requisitionlineitem_set-0-internal_price": 1,
            "requisitionlineitem_set-0-requisition": requisition.id,
            "requisitionlineitem_set-1-id": requisition.requisitionlineitem_set.last().id,
            "requisitionlineitem_set-1-product": product2.pk,
            "requisitionlineitem_set-1-quantity": 2,
            "requisitionlineitem_set-1-internal_price": 1,
            "requisitionlineitem_set-1-requisition": requisition.id,
        }

        res = self.client.post(url, data)
        requisition.refresh_from_db()
        self.assertEqual(850, requisition.total)
        self.assertEqual("Bar Supplies", requisition.title)
        self.assertEqual("Nice", requisition.review_reason)

    @patch("tiny_erp.apps.purchases.forms.timezone")
    def test_crispy_requisition_form(self, mocked):
        """Test crispy forms output."""
        now_mock = MagicMock()
        now_mock.date = date(2019, 6, 15)
        mocked.now.return_value = now_mock

        staffprofile = make_staffprofile(dict(user=self.user, id=99))
        user2 = baker.make("auth.User", first_name="Mosh", last_name="Pitt")
        make_staffprofile(dict(user=user2, id=999))

        self.assertMatchSnapshot(render_crispy_form(RequisitionForm))

        business = baker.make("locations.Business", name="Abc Ltd", id=99)
        location = baker.make("locations.Location", name="Voi", id=99)
        department = baker.make("locations.Department", name="Science", id=99)
        requisition = baker.make(
            "purchases.Requisition",
            title="Kitchen Supplies",
            staff=staffprofile,
            location=location,
            department=department,
            business=business,
            date_placed="2019-06-24",
            date_required="2019-06-24",
            id=99,
        )
        baker.make(
            "purchases.RequisitionLineItem",
            _quantity=1,
            item="Pen",
            quantity=2,
            internal_price=20,
            requisition=requisition,
            id=557,
        )

        self.assertMatchSnapshot(
            render_crispy_form(UpdateRequisitionForm(instance=requisition))
        )

    @patch("tiny_erp.apps.purchases.forms.timezone")
    def test_crispy_requisition_product_form(self, mocked):
        """Test crispy forms output."""
        now_mock = MagicMock()
        now_mock.date = date(2019, 6, 15)
        mocked.now.return_value = now_mock

        staffprofile = make_staffprofile(dict(user=self.user, id=99))
        user2 = baker.make("auth.User", first_name="Mosh", last_name="Pitt")
        make_staffprofile(dict(user=user2, id=999))

        product1 = baker.make(
            "products.product",
            name="Lego",
            internal_amount=99,
            id=776,
            sku="776",
            unit=baker.make("products.MeasurementUnit", name="Box", symbol="box"),
            supplier=baker.make("products.Supplier", name="GAP"),
        )
        baker.make(
            "products.product",
            name="Duvet",
            internal_amount=5000,
            id=777,
            sku="777",
            unit=baker.make("products.MeasurementUnit", name="Metre", symbol="m"),
            supplier=baker.make("products.Supplier", name="GAP"),
        )

        self.assertMatchSnapshot(render_crispy_form(RequisitionProductForm))

        business = baker.make("locations.Business", name="Abc Ltd", id=99)
        location = baker.make("locations.Location", name="Voi", id=99)
        department = baker.make("locations.Department", name="Science", id=99)
        requisition = baker.make(
            "purchases.Requisition",
            title="Kitchen Supplies",
            staff=staffprofile,
            location=location,
            department=department,
            business=business,
            date_placed="2019-06-24",
            date_required="2019-06-24",
            id=99,
        )
        baker.make(
            "purchases.RequisitionLineItem",
            _quantity=1,
            product=product1,
            item=product1.name,
            quantity=12,
            internal_price=product1.internal_amount,
            requisition=requisition,
            id=556,
        )

        self.assertMatchSnapshot(
            render_crispy_form(UpdatedRequisitionProductForm(instance=requisition))
        )

    def test_requisition_lineitem_form(self):
        """Test RequisitionLineItemForm."""
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        requisition = baker.make("purchases.Requisition", staff=staffprofile)

        data = {
            "requisition": requisition.id,
            "item": "Tubes",
            "quantity": 3,
            "internal_price": 200,
        }

        form = RequisitionLineItemForm(data=data)
        self.assertTrue(form.is_valid())
        item = form.save()
        self.assertEqual(requisition, item.requisition)
        self.assertEqual("Tubes", item.item)
        self.assertEqual(3, item.quantity)
        self.assertEqual(Money("200", "KES"), item.price)

    def test_requisition_lineitem_product_form(self):
        """Test RequisitionLineItemProductForm."""
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        requisition = baker.make("purchases.Requisition", staff=staffprofile)
        unit = baker.make("products.MeasurementUnit", name="Metre", symbol="m")
        supplier = baker.make("products.Supplier", name="GAP")
        product = baker.make(
            "products.Product",
            name="Pipes",
            internal_amount=123,
            unit=unit,
            supplier=supplier,
        )

        data = {
            "requisition": requisition.id,
            "product": product.pk,
            "quantity": 3,
            "internal_price": 1,
        }

        form = RequisitionLineItemProductForm(data=data)
        self.assertTrue(form.is_valid())
        item = form.save()
        self.assertEqual(requisition, item.requisition)
        self.assertEqual("Pipes", item.item)
        self.assertEqual(3, item.quantity)
        self.assertEqual(Money("123", "KES"), item.price)
        self.assertEqual(product, item.product)

    def test_custom_formset_class(self):
        """Test custom formset class."""
        CustomFormSet = inlineformset_factory(  # pylint: disable=invalid-name
            Requisition,
            RequisitionLineItem,
            form=RequisitionLineItemForm,
            extra=12,
            can_delete=True,
        )

        class CreateForm(RequisitionForm):
            """Some custom create form."""

            formset_class = CustomFormSet

        class UpdateForm(UpdateRequisitionForm):
            """Some custom update form."""

            formset_class = CustomFormSet

        staffprofile = baker.make("small_small_hr.StaffProfile", user=self.user)
        requisition = baker.make("purchases.Requisition", staff=staffprofile)

        self.assertEqual(CustomFormSet, CreateForm().formset_class)
        self.assertEqual(CustomFormSet, UpdateForm(instance=requisition).formset_class)

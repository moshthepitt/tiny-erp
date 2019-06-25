"""module to test tiny-erp forms"""
from datetime import date

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from crispy_forms.utils import render_crispy_form
from model_mommy import mommy

from tiny_erp.apps.purchases.forms import RequisitionForm, RequisitionLineItemForm

CREATE_FORM = """
<form id="requisition-form" method="post">
    <div>
        <div id="div_id_staff" class="form-group">
            <label for="id_staff" class="control-label  requiredField">
                Staff Member<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="staff" class="select form-control" required id="id_staff">
                    <option value="" selected>---------</option>

                </select>
            </div>
        </div>
        <div id="div_id_business" class="form-group">
            <label for="id_business" class="control-label  requiredField">
                Business<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="business" class="select form-control" required id="id_business">
                    <option value="" selected>---------</option>

                </select>
            </div>
        </div>
        <div id="div_id_location" class="form-group">
            <label for="id_location" class="control-label  requiredField">
                Location<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="location" class="select form-control" required id="id_location">
                    <option value="" selected>---------</option>

                </select>
            </div>
        </div>
        <div id="div_id_department" class="form-group">
            <label for="id_department" class="control-label  requiredField">
                Department<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="department" class="select form-control" required id="id_department">
                    <option value="" selected>---------</option>

                </select>
            </div>
        </div>
        <div id="div_id_date_placed" class="form-group">
            <label for="id_date_placed" class="control-label  requiredField">
                Date Placed<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <input type="text" name="date_placed" class="dateinput form-control" required id="id_date_placed"> </div>
        </div>
        <div id="div_id_date_required" class="form-group">
            <label for="id_date_required" class="control-label  requiredField">
                Date Required<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <input type="text" name="date_required" class="dateinput form-control" required id="id_date_required"> </div>
        </div>
        <fieldset>
            <legend>Requisition Items</legend>
            <table class="table">
                <input type="hidden" name="requisitionlineitem_set-TOTAL_FORMS" value="3" id="id_requisitionlineitem_set-TOTAL_FORMS">
                <input type="hidden" name="requisitionlineitem_set-INITIAL_FORMS" value="0" id="id_requisitionlineitem_set-INITIAL_FORMS">
                <input type="hidden" name="requisitionlineitem_set-MIN_NUM_FORMS" value="0" id="id_requisitionlineitem_set-MIN_NUM_FORMS">
                <input type="hidden" name="requisitionlineitem_set-MAX_NUM_FORMS" value="1000" id="id_requisitionlineitem_set-MAX_NUM_FORMS">
                <tr class="row1 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-0-id" id="id_requisitionlineitem_set-0-id">
                        <input type="hidden" name="requisitionlineitem_set-0-requisition" id="id_requisitionlineitem_set-0-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-item" class="form-group">
                                <label for="id_requisitionlineitem_set-0-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="text" name="requisitionlineitem_set-0-item" maxlength="255" class="textinput textInput form-control" id="id_requisitionlineitem_set-0-item"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-quantity" class="form-group">
                                <label for="id_requisitionlineitem_set-0-quantity" class="control-label  requiredField">
                                    Quantity<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-0-quantity" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-0-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-price" class="form-group">
                                <label for="id_requisitionlineitem_set-0-price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-0-price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-0-price"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div class="form-group">
                                <div id="div_id_requisitionlineitem_set-0-DELETE" class="checkbox">
                                    <label for="id_requisitionlineitem_set-0-DELETE" class="">
                                        <input type="checkbox" name="requisitionlineitem_set-0-DELETE" class="checkboxinput" id="id_requisitionlineitem_set-0-DELETE"> Delete
                                    </label>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr class="row2 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-1-id" id="id_requisitionlineitem_set-1-id">
                        <input type="hidden" name="requisitionlineitem_set-1-requisition" id="id_requisitionlineitem_set-1-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-item" class="form-group">
                                <label for="id_requisitionlineitem_set-1-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="text" name="requisitionlineitem_set-1-item" maxlength="255" class="textinput textInput form-control" id="id_requisitionlineitem_set-1-item"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-quantity" class="form-group">
                                <label for="id_requisitionlineitem_set-1-quantity" class="control-label  requiredField">
                                    Quantity<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-1-quantity" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-price" class="form-group">
                                <label for="id_requisitionlineitem_set-1-price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-1-price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-price"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div class="form-group">
                                <div id="div_id_requisitionlineitem_set-1-DELETE" class="checkbox">
                                    <label for="id_requisitionlineitem_set-1-DELETE" class="">
                                        <input type="checkbox" name="requisitionlineitem_set-1-DELETE" class="checkboxinput" id="id_requisitionlineitem_set-1-DELETE"> Delete
                                    </label>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr class="row1 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-2-id" id="id_requisitionlineitem_set-2-id">
                        <input type="hidden" name="requisitionlineitem_set-2-requisition" id="id_requisitionlineitem_set-2-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-item" class="form-group">
                                <label for="id_requisitionlineitem_set-2-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="text" name="requisitionlineitem_set-2-item" maxlength="255" class="textinput textInput form-control" id="id_requisitionlineitem_set-2-item"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-quantity" class="form-group">
                                <label for="id_requisitionlineitem_set-2-quantity" class="control-label  requiredField">
                                    Quantity<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-2-quantity" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-price" class="form-group">
                                <label for="id_requisitionlineitem_set-2-price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-2-price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-price"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div class="form-group">
                                <div id="div_id_requisitionlineitem_set-2-DELETE" class="checkbox">
                                    <label for="id_requisitionlineitem_set-2-DELETE" class="">
                                        <input type="checkbox" name="requisitionlineitem_set-2-DELETE" class="checkboxinput" id="id_requisitionlineitem_set-2-DELETE"> Delete
                                    </label>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
        </fieldset>
        <div id="div_id_reason" class="form-group">
            <label for="id_reason" class="control-label  requiredField">
                Reason<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <textarea name="reason" cols="40" rows="10" class="textarea form-control" required id="id_reason">
                </textarea>
            </div>
        </div>
        <br>
        <div class="buttonHolder">
            <input type="submit" name="submitBtn" value="Submit" class="btn btn-primary btn-primary" id="submit-id-submitbtn" />

        </div>

    </div>
</form>
"""  # noqa

EDIT_FORM = """
<form id="requisition-form" method="post">
    <div>
        <div id="div_id_staff" class="form-group">
            <label for="id_staff" class="control-label  requiredField">
                Staff Member<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="staff" class="select form-control" required id="id_staff">
                    <option value="">---------</option>
                    <option value="1" selected>Bob Ndoe</option>

                </select>
            </div>
        </div>
        <div id="div_id_business" class="form-group">
            <label for="id_business" class="control-label  requiredField">
                Business<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="business" class="select form-control" required id="id_business">
                    <option value="">---------</option>
                    <option value="1" selected>Abc Ltd</option>

                </select>
            </div>
        </div>
        <div id="div_id_location" class="form-group">
            <label for="id_location" class="control-label  requiredField">
                Location<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="location" class="select form-control" required id="id_location">
                    <option value="">---------</option>
                    <option value="1" selected>Voi</option>

                </select>
            </div>
        </div>
        <div id="div_id_department" class="form-group">
            <label for="id_department" class="control-label  requiredField">
                Department<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="department" class="select form-control" required id="id_department">
                    <option value="">---------</option>
                    <option value="1" selected>Science</option>

                </select>
            </div>
        </div>
        <div id="div_id_date_placed" class="form-group">
            <label for="id_date_placed" class="control-label  requiredField">
                Date Placed<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <input type="text" name="date_placed" value="2019-06-24" class="dateinput form-control" required id="id_date_placed"> </div>
        </div>
        <div id="div_id_date_required" class="form-group">
            <label for="id_date_required" class="control-label  requiredField">
                Date Required<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <input type="text" name="date_required" value="2019-06-24" class="dateinput form-control" required id="id_date_required"> </div>
        </div>
        <fieldset>
            <legend>Requisition Items</legend>
            <table class="table">
                <input type="hidden" name="requisitionlineitem_set-TOTAL_FORMS" value="4" id="id_requisitionlineitem_set-TOTAL_FORMS">
                <input type="hidden" name="requisitionlineitem_set-INITIAL_FORMS" value="1" id="id_requisitionlineitem_set-INITIAL_FORMS">
                <input type="hidden" name="requisitionlineitem_set-MIN_NUM_FORMS" value="0" id="id_requisitionlineitem_set-MIN_NUM_FORMS">
                <input type="hidden" name="requisitionlineitem_set-MAX_NUM_FORMS" value="1000" id="id_requisitionlineitem_set-MAX_NUM_FORMS">
                <tr class="row1 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-0-id" value="1" id="id_requisitionlineitem_set-0-id">
                        <input type="hidden" name="requisitionlineitem_set-0-requisition" value="1" id="id_requisitionlineitem_set-0-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-item" class="form-group">
                                <label for="id_requisitionlineitem_set-0-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="text" name="requisitionlineitem_set-0-item" value="Pen" maxlength="255" class="textinput textInput form-control" id="id_requisitionlineitem_set-0-item"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-quantity" class="form-group">
                                <label for="id_requisitionlineitem_set-0-quantity" class="control-label  requiredField">
                                    Quantity<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-0-quantity" value="2.00" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-0-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-price" class="form-group">
                                <label for="id_requisitionlineitem_set-0-price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-0-price" value="20.00" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-0-price"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div class="form-group">
                                <div id="div_id_requisitionlineitem_set-0-DELETE" class="checkbox">
                                    <label for="id_requisitionlineitem_set-0-DELETE" class="">
                                        <input type="checkbox" name="requisitionlineitem_set-0-DELETE" class="checkboxinput" id="id_requisitionlineitem_set-0-DELETE"> Delete
                                    </label>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr class="row2 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-1-id" id="id_requisitionlineitem_set-1-id">
                        <input type="hidden" name="requisitionlineitem_set-1-requisition" value="1" id="id_requisitionlineitem_set-1-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-item" class="form-group">
                                <label for="id_requisitionlineitem_set-1-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="text" name="requisitionlineitem_set-1-item" maxlength="255" class="textinput textInput form-control" id="id_requisitionlineitem_set-1-item"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-quantity" class="form-group">
                                <label for="id_requisitionlineitem_set-1-quantity" class="control-label  requiredField">
                                    Quantity<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-1-quantity" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-price" class="form-group">
                                <label for="id_requisitionlineitem_set-1-price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-1-price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-price"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div class="form-group">
                                <div id="div_id_requisitionlineitem_set-1-DELETE" class="checkbox">
                                    <label for="id_requisitionlineitem_set-1-DELETE" class="">
                                        <input type="checkbox" name="requisitionlineitem_set-1-DELETE" class="checkboxinput" id="id_requisitionlineitem_set-1-DELETE"> Delete
                                    </label>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr class="row1 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-2-id" id="id_requisitionlineitem_set-2-id">
                        <input type="hidden" name="requisitionlineitem_set-2-requisition" value="1" id="id_requisitionlineitem_set-2-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-item" class="form-group">
                                <label for="id_requisitionlineitem_set-2-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="text" name="requisitionlineitem_set-2-item" maxlength="255" class="textinput textInput form-control" id="id_requisitionlineitem_set-2-item"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-quantity" class="form-group">
                                <label for="id_requisitionlineitem_set-2-quantity" class="control-label  requiredField">
                                    Quantity<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-2-quantity" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-price" class="form-group">
                                <label for="id_requisitionlineitem_set-2-price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-2-price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-price"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div class="form-group">
                                <div id="div_id_requisitionlineitem_set-2-DELETE" class="checkbox">
                                    <label for="id_requisitionlineitem_set-2-DELETE" class="">
                                        <input type="checkbox" name="requisitionlineitem_set-2-DELETE" class="checkboxinput" id="id_requisitionlineitem_set-2-DELETE"> Delete
                                    </label>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr class="row2 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-3-id" id="id_requisitionlineitem_set-3-id">
                        <input type="hidden" name="requisitionlineitem_set-3-requisition" value="1" id="id_requisitionlineitem_set-3-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-3-item" class="form-group">
                                <label for="id_requisitionlineitem_set-3-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="text" name="requisitionlineitem_set-3-item" maxlength="255" class="textinput textInput form-control" id="id_requisitionlineitem_set-3-item"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-3-quantity" class="form-group">
                                <label for="id_requisitionlineitem_set-3-quantity" class="control-label  requiredField">
                                    Quantity<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-3-quantity" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-3-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-3-price" class="form-group">
                                <label for="id_requisitionlineitem_set-3-price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-3-price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-3-price"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div class="form-group">
                                <div id="div_id_requisitionlineitem_set-3-DELETE" class="checkbox">
                                    <label for="id_requisitionlineitem_set-3-DELETE" class="">
                                        <input type="checkbox" name="requisitionlineitem_set-3-DELETE" class="checkboxinput" id="id_requisitionlineitem_set-3-DELETE"> Delete
                                    </label>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
        </fieldset>
        <div id="div_id_reason" class="form-group">
            <label for="id_reason" class="control-label  requiredField">
                Reason<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <textarea name="reason" cols="40" rows="10" class="textarea form-control" required id="id_reason">
                </textarea>
            </div>
        </div>
        <br>
        <div class="buttonHolder">
            <input type="submit" name="submitBtn" value="Submit" class="btn btn-primary btn-primary" id="submit-id-submitbtn" />

        </div>

    </div>
</form>
"""  # noqa


class TestForms(TestCase):
    """
    Test class for forms
    """

    def setUp(self):
        """
        Setup test class
        """
        self.factory = RequestFactory()

    def test_requisition_form(self):
        """
        Test RequisitionForm
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

    def test_crispy_requisition_form(self):
        """
        Test crispy forms output
        """
        self.assertHTMLEqual(CREATE_FORM, render_crispy_form(RequisitionForm))

        user = mommy.make("auth.User", first_name="Bob", last_name="Ndoe")
        staffprofile = mommy.make("small_small_hr.StaffProfile", user=user)
        business = mommy.make("locations.Business", name="Abc Ltd")
        location = mommy.make("locations.Location", name="Voi")
        department = mommy.make("locations.Department", name="Science")
        requisition = mommy.make(
            "purchases.Requisition",
            staff=staffprofile,
            location=location,
            department=department,
            business=business,
            date_placed="2019-06-24",
            date_required="2019-06-24",
        )
        mommy.make(
            "purchases.RequisitionLineItem",
            _quantity=1,
            item="Pen",
            quantity=2,
            price=20,
            requisition=requisition,
        )

        self.assertHTMLEqual(
            EDIT_FORM, render_crispy_form(RequisitionForm(instance=requisition))
        )

    def test_requisition_lineitem_form(self):
        """
        Test RequisitionLineItemForm
        """
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        user = mommy.make("auth.User", first_name="Bob", last_name="Ndoe")
        staffprofile = mommy.make("small_small_hr.StaffProfile", user=user)
        requisition = mommy.make("purchases.Requisition", staff=staffprofile)

        data = {
            "requisition": requisition.id,
            "item": "Tubes",
            "quantity": 3,
            "price": 200,
        }

        form = RequisitionLineItemForm(data=data)
        self.assertTrue(form.is_valid())
        item = form.save()
        self.assertEqual(requisition, item.requisition)
        self.assertEqual("Tubes", item.item)
        self.assertEqual(3, item.quantity)
        self.assertEqual(200, item.price)

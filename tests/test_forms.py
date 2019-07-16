"""module to test tiny-erp forms"""
from datetime import date
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import AnonymousUser
from django.forms.models import inlineformset_factory
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from crispy_forms.utils import render_crispy_form
from model_mommy import mommy

from tiny_erp.apps.locations.models import Business, Department, Location
from tiny_erp.apps.purchases.forms import (
    RequisitionForm,
    RequisitionLineItemForm,
    UpdateRequisitionForm,
)
from tiny_erp.apps.purchases.models import Requisition, RequisitionLineItem

CREATE_FORM = """
<form id="requisition-form" method="post">
    <div>
        <div id="div_id_staff" class="form-group">
            <label for="id_staff" class="control-label  requiredField">
                Staff Member<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="staff" class="select form-control" required id="id_staff">
                    <option value="" selected>---------</option>
                    <option value="99">Bob Ndoe</option>
                    <option value="999">Mosh Pitt</option>

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
                <input type="text" name="date_placed" class="dateinput form-control" required id="id_date_placed" value="2019-06-15"> </div>
        </div>
        <div id="div_id_date_required" class="form-group">
            <label for="id_date_required" class="control-label  requiredField">
                Date Required<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <input type="text" name="date_required" class="dateinput form-control" required id="id_date_required"> </div>
        </div>
        <fieldset>
            <legend>Requisition Items</legend>
            <table class="table tiny-erp">
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
                                    <textarea name="requisitionlineitem_set-0-item" cols="40" rows="2" class="minitextarea form-control" id="id_requisitionlineitem_set-0-item">
                                    </textarea>
                                </div>
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
                                    <textarea name="requisitionlineitem_set-1-item" cols="40" rows="2" class="minitextarea form-control" id="id_requisitionlineitem_set-1-item">
                                    </textarea>
                                </div>
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
                                    <textarea name="requisitionlineitem_set-2-item" cols="40" rows="2" class="minitextarea form-control" id="id_requisitionlineitem_set-2-item">
                                    </textarea>
                                </div>
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
<form id="requisition-update-form" method="post">
    <div>
        <input type="hidden" name="staff" value="99" id="id_staff">
        <div id="div_id_business" class="form-group">
            <label for="id_business" class="control-label  requiredField">
                Business<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="business" class="select form-control" required id="id_business">
                    <option value="">---------</option>
                    <option value="99" selected>Abc Ltd</option>

                </select>
            </div>
        </div>
        <div id="div_id_location" class="form-group">
            <label for="id_location" class="control-label  requiredField">
                Location<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="location" class="select form-control" required id="id_location">
                    <option value="">---------</option>
                    <option value="99" selected>Voi</option>

                </select>
            </div>
        </div>
        <div id="div_id_department" class="form-group">
            <label for="id_department" class="control-label  requiredField">
                Department<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <select name="department" class="select form-control" required id="id_department">
                    <option value="">---------</option>
                    <option value="99" selected>Science</option>

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
        <div id="div_id_status" class="form-group">
            <label for="id_status" class="control-label ">
                Status
            </label>
            <div class="controls ">
                <select name="status" class="select form-control" id="id_status">
                    <option value="">---------</option>
                    <option value="1">Approved</option>
                    <option value="3" selected>Pending</option>
                    <option value="2">Rejected</option>

                </select>
            </div>
        </div>
        <fieldset>
            <legend>Requisition Items</legend>
            <table class="table tiny-erp">
                <input type="hidden" name="requisitionlineitem_set-TOTAL_FORMS" value="4" id="id_requisitionlineitem_set-TOTAL_FORMS">
                <input type="hidden" name="requisitionlineitem_set-INITIAL_FORMS" value="1" id="id_requisitionlineitem_set-INITIAL_FORMS">
                <input type="hidden" name="requisitionlineitem_set-MIN_NUM_FORMS" value="0" id="id_requisitionlineitem_set-MIN_NUM_FORMS">
                <input type="hidden" name="requisitionlineitem_set-MAX_NUM_FORMS" value="1000" id="id_requisitionlineitem_set-MAX_NUM_FORMS">
                <tr class="row1 formset_row-requisitionlineitem_set">
                    <td>
                        <input type="hidden" name="requisitionlineitem_set-0-id" value="1" id="id_requisitionlineitem_set-0-id">
                        <input type="hidden" name="requisitionlineitem_set-0-requisition" value="99" id="id_requisitionlineitem_set-0-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-item" class="form-group">
                                <label for="id_requisitionlineitem_set-0-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <textarea name="requisitionlineitem_set-0-item" cols="40" rows="2" class="minitextarea form-control" id="id_requisitionlineitem_set-0-item">
                                        Pen</textarea>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-1-requisition" value="99" id="id_requisitionlineitem_set-1-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-item" class="form-group">
                                <label for="id_requisitionlineitem_set-1-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <textarea name="requisitionlineitem_set-1-item" cols="40" rows="2" class="minitextarea form-control" id="id_requisitionlineitem_set-1-item">
                                    </textarea>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-2-requisition" value="99" id="id_requisitionlineitem_set-2-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-item" class="form-group">
                                <label for="id_requisitionlineitem_set-2-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <textarea name="requisitionlineitem_set-2-item" cols="40" rows="2" class="minitextarea form-control" id="id_requisitionlineitem_set-2-item">
                                    </textarea>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-3-requisition" value="99" id="id_requisitionlineitem_set-3-requisition">
                        <div>
                            <div id="div_id_requisitionlineitem_set-3-item" class="form-group">
                                <label for="id_requisitionlineitem_set-3-item" class="control-label  requiredField">
                                    Item<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <textarea name="requisitionlineitem_set-3-item" cols="40" rows="2" class="minitextarea form-control" id="id_requisitionlineitem_set-3-item">
                                    </textarea>
                                </div>
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
        <div id="div_id_comments" class="form-group">
            <label for="id_comments" class="control-label ">
                Comments
            </label>
            <div class="controls ">
                <textarea name="comments" cols="40" rows="10" class="textarea form-control" id="id_comments">
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


@override_settings(
    TINY_ERP_REQUISITION_ITEMS_TXT="Requisition Items", TINY_ERP_SUBMIT_TXT="Submit"
)
class TestForms(TestCase):
    """
    Test class for forms
    """

    maxDiff = None

    def setUp(self):
        """
        Setup test class
        """
        self.factory = RequestFactory()
        Business.objects.all().delete()
        Department.objects.all().delete()
        Location.objects.all().delete()

    @patch("tiny_erp.apps.purchases.forms.requisition_approved_email")
    @patch("tiny_erp.apps.purchases.forms.requisition_updated_email")
    @patch("tiny_erp.apps.purchases.forms.requisition_filed_email")
    def test_requisition_form(self, filed_mock, updated_mock, approved_mock):
        """
        Test RequisitionForm
        """
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        user = mommy.make("auth.User", first_name="Bob", last_name="Ndoe")
        staffprofile = mommy.make("small_small_hr.StaffProfile", user=user)
        mommy.make("small_small_hr.StaffProfile", _quantity=2)
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

        self.assertEqual(1, filed_mock.call_count)
        self.assertEqual(0, updated_mock.call_count)
        self.assertEqual(0, approved_mock.call_count)
        filed_mock.assert_called_with(requisition_obj=requisition)

    @patch("tiny_erp.apps.purchases.forms.requisition_approved_email")
    @patch("tiny_erp.apps.purchases.forms.requisition_updated_email")
    @patch("tiny_erp.apps.purchases.forms.requisition_filed_email")
    def test_updated_requisition_form(self, filed_mock, updated_mock, approved_mock):
        """
        Test UpdateRequisitionForm
        """
        request = self.factory.get("/")
        request.session = {}
        request.user = AnonymousUser()

        user = mommy.make("auth.User", first_name="Bob", last_name="Ndoe")
        staffprofile = mommy.make("small_small_hr.StaffProfile", user=user)
        mommy.make("small_small_hr.StaffProfile", _quantity=2)
        business = mommy.make("locations.Business", name="X Inc")
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
            id=99,
        )

        data = {
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "reason": "changed this",
        }
        form = UpdateRequisitionForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("changed this", requisition.reason)
        self.assertEqual(0, filed_mock.call_count)
        self.assertEqual(1, updated_mock.call_count)
        self.assertEqual(0, approved_mock.call_count)
        updated_mock.assert_called_with(requisition_obj=requisition)

        data = {
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "status": Requisition.REJECTED,
            "reason": "Not good",
        }
        form = UpdateRequisitionForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Not good", requisition.reason)
        self.assertEqual(Requisition.REJECTED, requisition.status)
        self.assertEqual(0, filed_mock.call_count)
        self.assertEqual(2, updated_mock.call_count)
        self.assertEqual(0, approved_mock.call_count)
        updated_mock.assert_called_with(requisition_obj=requisition)

        data = {
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "status": Requisition.APPROVED,
            "reason": "Great",
        }
        form = UpdateRequisitionForm(instance=requisition, data=data)
        requisition = form.save()

        self.assertEqual("Great", requisition.reason)
        self.assertEqual(Requisition.APPROVED, requisition.status)
        self.assertEqual(0, filed_mock.call_count)
        self.assertEqual(2, updated_mock.call_count)
        self.assertEqual(1, approved_mock.call_count)
        approved_mock.assert_called_with(requisition_obj=requisition)

    @override_settings(ROOT_URLCONF="tests.crud")
    def test_full_requisition_form(self):
        """
        Test the full implementation of the requesition form
        """
        Requisition.objects.all().delete()
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
            "reason": "I love oov",
            "total": 0,
            "requisitionlineitem_set-TOTAL_FORMS": 3,
            "requisitionlineitem_set-INITIAL_FORMS": 0,
            "requisitionlineitem_set-MIN_NUM_FORMS": 0,
            "requisitionlineitem_set-0-item": "Pen",
            "requisitionlineitem_set-0-quantity": 3,
            "requisitionlineitem_set-0-price": 7,
            "requisitionlineitem_set-1-item": "Ink",
            "requisitionlineitem_set-1-quantity": 1,
            "requisitionlineitem_set-1-price": 20,
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
        self.assertEqual(Requisition.PENDING, requisition.status)
        self.assertEqual("I love oov", requisition.reason)
        self.assertEqual("", requisition.comments)

        url = reverse("purchases.requisition-update", kwargs={"pk": requisition.id})
        data = {
            "id": requisition.id,
            "staff": staffprofile.id,
            "location": location.id,
            "business": business.id,
            "department": department.id,
            "date_placed": "01/01/2019",
            "date_required": "02/02/2019",
            "total": 0,
            "reason": "Nice",
            "comments": "Shall order on the 25th.",
            "status": Requisition.APPROVED,
            "requisitionlineitem_set-TOTAL_FORMS": 5,
            "requisitionlineitem_set-INITIAL_FORMS": 2,
            "requisitionlineitem_set-MIN_NUM_FORMS": 0,
            "requisitionlineitem_set-MAX_NUM_FORMS": 1000,
            "requisitionlineitem_set-0-id": requisition.requisitionlineitem_set.first().id,  # noqa
            "requisitionlineitem_set-0-item": "Pen",
            "requisitionlineitem_set-0-quantity": 3,
            "requisitionlineitem_set-0-price": 7,
            "requisitionlineitem_set-0-requisition": requisition.id,
            "requisitionlineitem_set-1-id": requisition.requisitionlineitem_set.last().id,
            "requisitionlineitem_set-1-item": "Ink",
            "requisitionlineitem_set-1-quantity": 1,
            "requisitionlineitem_set-1-price": 20,
            "requisitionlineitem_set-1-DELETE": "1",  # this line item is e=being deleted
            "requisitionlineitem_set-1-requisition": requisition.id,
            "requisitionlineitem_set-2-item": "Pencil",
            "requisitionlineitem_set-2-quantity": 8,
            "requisitionlineitem_set-2-price": 17,
            "requisitionlineitem_set-2-requisition": requisition.id,
        }

        res = self.client.post(url, data)
        requisition.refresh_from_db()
        self.assertEqual(157, requisition.total)
        self.assertEqual(Requisition.APPROVED, requisition.status)
        self.assertEqual("Nice", requisition.reason)
        self.assertEqual("Shall order on the 25th.", requisition.comments)

    @patch("tiny_erp.apps.purchases.forms.timezone")
    def test_crispy_requisition_form(self, mocked):
        """
        Test crispy forms output
        """
        now_mock = MagicMock()
        now_mock.date = date(2019, 6, 15)
        mocked.now.return_value = now_mock

        user = mommy.make("auth.User", first_name="Bob", last_name="Ndoe")
        staffprofile = mommy.make("small_small_hr.StaffProfile", user=user, id=99)
        user2 = mommy.make("auth.User", first_name="Mosh", last_name="Pitt")
        mommy.make("small_small_hr.StaffProfile", user=user2, id=999)

        self.assertHTMLEqual(CREATE_FORM, render_crispy_form(RequisitionForm))
        business = mommy.make("locations.Business", name="Abc Ltd", id=99)
        location = mommy.make("locations.Location", name="Voi", id=99)
        department = mommy.make("locations.Department", name="Science", id=99)
        requisition = mommy.make(
            "purchases.Requisition",
            staff=staffprofile,
            location=location,
            department=department,
            business=business,
            date_placed="2019-06-24",
            date_required="2019-06-24",
            id=99,
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
            EDIT_FORM, render_crispy_form(UpdateRequisitionForm(instance=requisition))
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

    def test_custom_formset_class(self):
        """Test custom formset class"""
        CustomFormSet = inlineformset_factory(  # pylint: disable=invalid-name
            Requisition,
            RequisitionLineItem,
            form=RequisitionLineItemForm,
            fields=["item", "quantity", "price"],
            extra=12,
            can_delete=True,
        )

        class CreateForm(RequisitionForm):
            """Some custom create form"""

            formset_class = CustomFormSet

        class UpdateForm(UpdateRequisitionForm):
            """Some custom update form"""

            formset_class = CustomFormSet

        user = mommy.make("auth.User", first_name="Bob", last_name="Ndoe")
        staffprofile = mommy.make("small_small_hr.StaffProfile", user=user)
        requisition = mommy.make("purchases.Requisition", staff=staffprofile)

        self.assertEqual(CustomFormSet, CreateForm().formset_class)
        self.assertEqual(CustomFormSet, UpdateForm(instance=requisition).formset_class)

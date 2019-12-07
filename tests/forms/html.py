"""HTML strings."""

CREATE_FORM = """
<form id="requisition-form" method="post">
    <div>
        <div id="div_id_title" class="form-group">
            <label for="id_title" class="control-label  requiredField">
                Title<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <input type="text" name="title" maxlength="255" class="textinput textInput form-control" required id="id_title"> </div>
        </div>
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
                <input type="text" name="date_placed" value="2019-06-15" class="dateinput form-control" required id="id_date_placed"> </div>
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
                        <input type="hidden" name="requisitionlineitem_set-0-requisition" id="id_requisitionlineitem_set-0-requisition">
                        <input type="hidden" name="requisitionlineitem_set-0-id" id="id_requisitionlineitem_set-0-id">
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
                                    <input type="number" name="requisitionlineitem_set-0-quantity" value="1" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-0-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-0-internal_price" class="form-group">
                                <label for="id_requisitionlineitem_set-0-internal_price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-0-internal_price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-0-internal_price">
                                    <div id="hint_id_requisitionlineitem_set-0-internal_price" class="help-block">The price per item</div>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-1-requisition" id="id_requisitionlineitem_set-1-requisition">
                        <input type="hidden" name="requisitionlineitem_set-1-id" id="id_requisitionlineitem_set-1-id">
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
                                    <input type="number" name="requisitionlineitem_set-1-quantity" value="1" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-internal_price" class="form-group">
                                <label for="id_requisitionlineitem_set-1-internal_price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-1-internal_price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-internal_price">
                                    <div id="hint_id_requisitionlineitem_set-1-internal_price" class="help-block">The price per item</div>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-2-requisition" id="id_requisitionlineitem_set-2-requisition">
                        <input type="hidden" name="requisitionlineitem_set-2-id" id="id_requisitionlineitem_set-2-id">
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
                                    <input type="number" name="requisitionlineitem_set-2-quantity" value="1" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-internal_price" class="form-group">
                                <label for="id_requisitionlineitem_set-2-internal_price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-2-internal_price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-internal_price">
                                    <div id="hint_id_requisitionlineitem_set-2-internal_price" class="help-block">The price per item</div>
                                </div>
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
        <div id="div_id_title" class="form-group">
            <label for="id_title" class="control-label  requiredField">
                Title<span class="asteriskField">*</span> </label>
            <div class="controls ">
                <input type="text" name="title" value="Kitchen Supplies" maxlength="255" class="textinput textInput form-control" required id="id_title"> </div>
        </div>
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
                        <input type="hidden" name="requisitionlineitem_set-0-requisition" value="99" id="id_requisitionlineitem_set-0-requisition">
                        <input type="hidden" name="requisitionlineitem_set-0-id" value="1" id="id_requisitionlineitem_set-0-id">
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
                            <div id="div_id_requisitionlineitem_set-0-internal_price" class="form-group">
                                <label for="id_requisitionlineitem_set-0-internal_price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-0-internal_price" value="20.00" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-0-internal_price">
                                    <div id="hint_id_requisitionlineitem_set-0-internal_price" class="help-block">The price per item</div>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-1-requisition" value="99" id="id_requisitionlineitem_set-1-requisition">
                        <input type="hidden" name="requisitionlineitem_set-1-id" id="id_requisitionlineitem_set-1-id">
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
                                    <input type="number" name="requisitionlineitem_set-1-quantity" value="1" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-1-internal_price" class="form-group">
                                <label for="id_requisitionlineitem_set-1-internal_price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-1-internal_price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-1-internal_price">
                                    <div id="hint_id_requisitionlineitem_set-1-internal_price" class="help-block">The price per item</div>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-2-requisition" value="99" id="id_requisitionlineitem_set-2-requisition">
                        <input type="hidden" name="requisitionlineitem_set-2-id" id="id_requisitionlineitem_set-2-id">
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
                                    <input type="number" name="requisitionlineitem_set-2-quantity" value="1" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-2-internal_price" class="form-group">
                                <label for="id_requisitionlineitem_set-2-internal_price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-2-internal_price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-2-internal_price">
                                    <div id="hint_id_requisitionlineitem_set-2-internal_price" class="help-block">The price per item</div>
                                </div>
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
                        <input type="hidden" name="requisitionlineitem_set-3-requisition" value="99" id="id_requisitionlineitem_set-3-requisition">
                        <input type="hidden" name="requisitionlineitem_set-3-id" id="id_requisitionlineitem_set-3-id">
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
                                    <input type="number" name="requisitionlineitem_set-3-quantity" value="1" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-3-quantity"> </div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div>
                            <div id="div_id_requisitionlineitem_set-3-internal_price" class="form-group">
                                <label for="id_requisitionlineitem_set-3-internal_price" class="control-label  requiredField">
                                    Price<span class="asteriskField">*</span> </label>
                                <div class="controls ">
                                    <input type="number" name="requisitionlineitem_set-3-internal_price" step="0.01" class="numberinput form-control" id="id_requisitionlineitem_set-3-internal_price">
                                    <div id="hint_id_requisitionlineitem_set-3-internal_price" class="help-block">The price per item</div>
                                </div>
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

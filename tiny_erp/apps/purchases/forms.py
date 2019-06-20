"""Forms module for tiny erp"""
from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Field, Fieldset, Layout, Submit

from tiny_erp.apps.purchases.models import Requisition, RequisitionLineItem
from tiny_erp.layout import Formset


class RequisitionLineItemForm(forms.ModelForm):
    """Form definition for RequisitionLineItem."""

    class Meta:
        """Meta definition for RequisitionLineItemform."""

        model = RequisitionLineItem
        fields = ["item", "quantity", "price"]


RequisitionItemFormSet = inlineformset_factory(  # pylint: disable=invalid-name
    Requisition,
    RequisitionLineItem,
    form=RequisitionLineItemForm,
    fields=["item", "quantity", "price"],
    extra=3,
    can_delete=True,
)


class RequisitionForm(forms.ModelForm):
    """Form definition for Requisition."""

    class Meta:
        """Meta definition for Requisitionform."""

        model = Requisition
        fields = [
            "name",
            "staff",
            "business",
            "location",
            "department",
            "date_placed",
            "date_required",
            "reason",
            "total",
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = "POST"
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.html5_required = True
        self.helper.form_id = "requisition-form"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.layout = Layout(
            Div(
                Field("name"),
                Field("staff"),
                Field("business"),
                Field("location"),
                Field("department"),
                Field("date_placed"),
                Field("date_required"),
                Fieldset("Requisition Items", Formset(RequisitionItemFormSet())),
                Field("reason"),
                Field("total"),
                HTML("<br>"),
                ButtonHolder(Submit("submit", "save")),
            )
        )

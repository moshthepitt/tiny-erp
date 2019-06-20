"""Forms module for tiny erp"""
from django import forms
from django.forms.models import inlineformset_factory

from tiny_erp.apps.purchases.models import Requisition, RequisitionLineItem


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

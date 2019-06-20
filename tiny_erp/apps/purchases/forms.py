"""
Forms module for tiny erp
"""
from django import forms

from tiny_erp.apps.purchases.models import Requisition, RequisitionLineItem


class RequisitionLineItemForm(forms.ModelForm):
    """Form definition for RequisitionLineItem."""

    class Meta:
        """Meta definition for RequisitionLineItemform."""

        model = RequisitionLineItem
        fields = ["item", "quantity", "price"]


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

"""
Forms module for tiny erp
"""
from django import forms

from tiny_erp.apps.purchases.models import Requisition


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

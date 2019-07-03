"""Forms module for tiny erp"""
from django import forms
from django.conf import settings
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _

from small_small_hr.models import StaffProfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Field, Fieldset, Layout, Submit

from tiny_erp.apps.purchases.emails import (
    requisition_approved_email,
    requisition_filed_email,
    requisition_updated_email,
)
from tiny_erp.apps.purchases.models import Requisition, RequisitionLineItem
from tiny_erp.layout import Formset


class RequisitionLineItemForm(forms.ModelForm):
    """Form definition for RequisitionLineItem."""

    class Meta:
        """Meta definition for RequisitionLineItemform."""

        model = RequisitionLineItem
        fields = ["requisition", "item", "quantity", "price"]


RequisitionItemFormSet = inlineformset_factory(  # pylint: disable=invalid-name
    Requisition,
    RequisitionLineItem,
    form=RequisitionLineItemForm,
    fields=["item", "quantity", "price"],
    extra=3,
    can_delete=True,
)


class SomeMixin:
    """Some mixin
    """

    def send_email(self, requisition):
        """Send email"""
        if not self.get_initial_for_field(self.fields["staff"], "staff"):
            # new requisition
            requisition_filed_email(requisition_obj=requisition)
        else:
            if requisition.status == Requisition.APPROVED:
                requisition_approved_email(requisition_obj=requisition)
            else:
                requisition_updated_email(requisition_obj=requisition)

    def clean(self):
        """ModelForm clean method"""
        cleaned_data = super().clean()
        self.formset = None
        if self.request:
            self.formset = RequisitionItemFormSet(
                self.request.POST, instance=self.instance
            )
            if not self.formset.is_valid():
                raise forms.ValidationError(
                    settings.TINY_ERP_REQUISITION_FORMSET_ERROR_TXT
                )
        return cleaned_data

    def save(self, commit=True):  # pylint: disable=unused-argument
        """
        Custom save method
        """
        with transaction.atomic():
            requisition = super().save()
            if self.formset:
                self.formset.save()

        requisition.set_total()
        self.send_email(requisition)

        return requisition


class RequisitionForm(SomeMixin, forms.ModelForm):
    """Form definition for Requisition."""

    class Meta:
        """Meta definition for Requisitionform."""

        model = Requisition
        fields = [
            "staff",
            "business",
            "location",
            "department",
            "date_placed",
            "date_required",
            "reason",
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.vega_extra_kwargs = kwargs.pop("vega_extra_kwargs", dict())
        super().__init__(*args, **kwargs)
        if self.request:
            # pylint: disable=no-member
            try:
                self.request.user.staffprofile
            except StaffProfile.DoesNotExist:
                pass
            except AttributeError:
                pass
            else:
                self.fields["staff"].queryset = StaffProfile.objects.filter(
                    id=self.request.user.staffprofile.id
                )
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = "POST"
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = "requisition-form"
        self.helper.layout = Layout(
            Div(
                Field("staff"),
                Field("business"),
                Field("location"),
                Field("department"),
                Field("date_placed"),
                Field("date_required"),
                Fieldset(
                    _(settings.TINY_ERP_REQUISITION_ITEMS_TXT),
                    Formset(
                        formset_in_context=RequisitionItemFormSet(
                            instance=self.instance
                        )
                    ),
                ),
                Field("reason"),
                HTML("<br>"),
                ButtonHolder(
                    Submit(
                        "submitBtn",
                        _(settings.TINY_ERP_SUBMIT_TXT),
                        css_class="btn-primary",
                    )
                ),
            )
        )


class UpdateRequisitionForm(SomeMixin, forms.ModelForm):
    """Form definition for Upodate Requisition."""

    class Meta:
        """Meta definition for UpdateRequisitionForm."""

        model = Requisition
        fields = [
            "staff",
            "business",
            "location",
            "department",
            "date_placed",
            "date_required",
            "reason",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.vega_extra_kwargs = kwargs.pop("vega_extra_kwargs", dict())
        super().__init__(*args, **kwargs)
        self.fields["staff"].queryset = StaffProfile.objects.filter(
            id=self.instance.staff.id
        )
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = "POST"
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = "requisition-update-form"
        self.helper.layout = Layout(
            Div(
                Field("staff", type="hidden"),
                Field("business"),
                Field("location"),
                Field("department"),
                Field("date_placed"),
                Field("date_required"),
                Field("status"),
                Fieldset(
                    _(settings.TINY_ERP_REQUISITION_ITEMS_TXT),
                    Formset(
                        formset_in_context=RequisitionItemFormSet(
                            instance=self.instance
                        )
                    ),
                ),
                Field("reason"),
                HTML("<br>"),
                ButtonHolder(
                    Submit(
                        "submitBtn",
                        _(settings.TINY_ERP_SUBMIT_TXT),
                        css_class="btn-primary",
                    )
                ),
            )
        )

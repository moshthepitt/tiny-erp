"""Forms module for tiny erp."""
from django import forms
from django.conf import settings
from django.db import transaction
from django.forms.models import ModelChoiceIterator, inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext as _

from small_small_hr.models import StaffProfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Field, Fieldset, Layout, Submit

from tiny_erp.apps.products.models import Product
from tiny_erp.apps.purchases.emails import (
    requisition_approved_email,
    requisition_filed_email,
    requisition_updated_email,
)
from tiny_erp.apps.purchases.models import Requisition, RequisitionLineItem
from tiny_erp.layout import Formset
from tiny_erp.widgets import MiniTextarea


class CustomModelChoiceIterator(
    # pylint: disable=too-few-public-methods,bad-continuation
    ModelChoiceIterator
):
    """Custom ModelChoiceIterator."""

    def choice(self, obj):
        """Return choice."""
        return (self.field.prepare_value(obj), self.field.label_from_instance(obj), obj)


class CustomModelChoiceField(forms.ModelChoiceField):
    """Custom ModelChoiceField."""

    iterator = CustomModelChoiceIterator

    def label_from_instance(self, obj):
        """
        Convert objects into strings and generate the labels for choices.

        Convert objects into strings and generate the labels for the choices
        presented by this object. Subclasses can override this method to
        customize the display of the choices.
        """
        return f"{obj.name} - {obj.unit.name} - {obj.supplier.name}"


class CustomSelect(forms.Select):
    """Custom Select."""

    option_template_name = "tiny_erp/product_option.html"

    def optgroups(self, name, value, attrs=None):  # pylint: disable=too-many-locals
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False

        for index, option_tuple in enumerate(self.choices):
            option_value = option_tuple[0]
            option_label = option_tuple[1]

            try:
                option_object = option_tuple[2]
            except IndexError:
                option_object = None

            if option_value is None:
                option_value = ""

            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = str(subvalue) in value and (
                    not has_selected or self.allow_multiple_selected
                )
                has_selected |= selected
                option = self.create_option(
                    name,
                    subvalue,
                    sublabel,
                    selected,
                    index,
                    subindex=subindex,
                    attrs=attrs,
                )
                option["object"] = option_object
                subgroup.append(option)
                if subindex is not None:
                    subindex += 1

        return groups


class RequisitionLineItemForm(forms.ModelForm):
    """Form definition for RequisitionLineItem."""

    class Meta:
        """Meta definition for RequisitionLineItemform."""

        model = RequisitionLineItem
        fields = ["requisition", "item", "quantity", "internal_price"]
        widgets = {"item": MiniTextarea()}


class RequisitionLineItemProductForm(forms.ModelForm):
    """Form definition for RequisitionLineItem that uses products."""

    product = CustomModelChoiceField(
        queryset=Product.objects.all(),
        label=_("Product"),
        required=True,
        widget=CustomSelect,
    )

    class Meta:
        """Meta definition for RequisitionLineItemform."""

        model = RequisitionLineItem
        fields = ["requisition", "product", "internal_price", "quantity"]

    def save(self, commit=False):  # pylint: disable=unused-argument
        """Save the form."""
        obj = super().save(commit)
        if obj.product:
            obj.item = obj.product.name
            obj.description = obj.product.description
            obj.currency = obj.product.currency
            obj.internal_price = obj.product.internal_amount
        obj.save()
        return obj


RequisitionItemFormSet = inlineformset_factory(  # pylint: disable=invalid-name
    Requisition,
    RequisitionLineItem,
    form=RequisitionLineItemForm,
    extra=3,
    can_delete=True,
)

RequisitionItemProductFormSet = inlineformset_factory(  # pylint: disable=invalid-name
    Requisition,
    RequisitionLineItem,
    form=RequisitionLineItemProductForm,
    extra=3,
    can_delete=True,
)


class RequisitionFormMixin:
    """Requisition Form mixin."""

    formset_class = RequisitionItemFormSet

    def send_email(self, requisition):
        """Send email."""
        if not self.get_initial_for_field(self.fields["staff"], "staff"):
            # new requisition
            requisition_filed_email(requisition_obj=requisition)
        else:
            if requisition.review_status == Requisition.APPROVED:
                requisition_approved_email(requisition_obj=requisition)
            else:
                requisition_updated_email(requisition_obj=requisition)

    def clean(self):
        """Clean the form."""
        cleaned_data = super().clean()
        self.formset = None
        if self.request:
            self.formset = self.formset_class(self.request.POST, instance=self.instance)
            if not self.formset.is_valid():
                raise forms.ValidationError(
                    settings.TINY_ERP_REQUISITION_FORMSET_ERROR_TXT
                )
        return cleaned_data

    def save(self, commit=True):  # pylint: disable=unused-argument
        """Save the form."""
        with transaction.atomic():
            requisition = super().save()
            if self.formset:
                self.formset.save()

        requisition.set_total()
        self.send_email(requisition)

        return requisition


class RequisitionForm(RequisitionFormMixin, forms.ModelForm):
    """Form definition for Requisition."""

    class Meta:
        """Meta definition for Requisitionform."""

        model = Requisition
        fields = [
            "title",
            "staff",
            "business",
            "location",
            "department",
            "date_placed",
            "date_required",
            "review_reason",
        ]

    def __init__(self, *args, **kwargs):
        """Initialize."""
        self.request = kwargs.pop("request", None)
        self.vega_extra_kwargs = kwargs.pop("vega_extra_kwargs", dict())
        super().__init__(*args, **kwargs)
        self.fields["date_placed"].initial = timezone.now().date
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
                Field("title"),
                Field("staff"),
                Field("business"),
                Field("location"),
                Field("department"),
                Field("date_placed"),
                Field("date_required"),
                Fieldset(
                    _(settings.TINY_ERP_REQUISITION_ITEMS_TXT),
                    Formset(
                        formset_in_context=self.formset_class(instance=self.instance)
                    ),
                ),
                Field("review_reason"),
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


class RequisitionProductForm(RequisitionForm):
    """Form definition for Requisition that uses products."""

    formset_class = RequisitionItemProductFormSet


class UpdateRequisitionForm(RequisitionFormMixin, forms.ModelForm):
    """Form definition for Update Requisition."""

    class Meta:
        """Meta definition for UpdateRequisitionForm."""

        model = Requisition
        fields = [
            "title",
            "staff",
            "business",
            "location",
            "department",
            "date_placed",
            "date_required",
            "review_reason",
            "review_status",
        ]

    def __init__(self, *args, **kwargs):
        """Initialize."""
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
                Field("title"),
                Field("staff", type="hidden"),
                Field("business"),
                Field("location"),
                Field("department"),
                Field("date_placed"),
                Field("date_required"),
                Field("review_status"),
                Fieldset(
                    _(settings.TINY_ERP_REQUISITION_ITEMS_TXT),
                    Formset(
                        formset_in_context=self.formset_class(instance=self.instance)
                    ),
                ),
                Field("review_reason"),
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


class UpdatedRequisitionProductForm(UpdateRequisitionForm):
    """Form definition for Requisition that uses products."""

    formset_class = RequisitionItemProductFormSet

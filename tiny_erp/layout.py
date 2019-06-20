"""Custom crispy forms layout objects"""
from typing import List

from django.template.loader import render_to_string

from crispy_forms.layout import TEMPLATE_PACK, LayoutObject


class Formset(LayoutObject):
    """Custom layout object to render Formsets"""

    template = "tiny_erp/formset.html"

    def __init__(self, formset_name_in_context: str, template: str = None):
        """init method"""
        self.formset_name_in_context = formset_name_in_context
        self.fields: List[str] = []
        if template:
            self.template = template

    def render(  # pylint: disable=unused-argument,bad-continuation
        self, form, form_style, context, template_pack=TEMPLATE_PACK
    ):
        """render method"""
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {"formset": formset})

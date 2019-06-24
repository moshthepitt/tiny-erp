"""Custom crispy forms layout objects"""
from django.template.loader import render_to_string

from crispy_forms.layout import TEMPLATE_PACK, LayoutObject


class Formset(LayoutObject):
    """Custom layout object to render Formsets"""

    template = "tiny_erp/formset.html"

    def __init__(self, formset_in_context: str, template: str = None):
        """init method"""
        self.formset_in_context = formset_in_context
        if template:
            self.template = template

    def render(  # pylint: disable=unused-argument,bad-continuation
        self, form, form_style, context, template_pack=TEMPLATE_PACK
    ):
        """render method"""

        return render_to_string(self.template, {"formset": self.formset_in_context})

"""Custom crispy forms layout objects"""
from django.template.loader import render_to_string

from crispy_forms.layout import LayoutObject


class Formset(LayoutObject):
    """Custom layout object to render Formsets"""

    template = "tiny_erp/formset.html"

    def __init__(self, formset_in_context: str, template: str = None):
        """[summary]

        Arguments:
            formset_in_context {str} -- The Formset object/class

        Keyword Arguments:
            template {str} -- The formset custom template path (default: {None})
        """
        self.formset_in_context = formset_in_context
        if template:
            self.template = template

    def render(self, *args, **kwargs):  # pylint: disable=unused-argument
        """the render method"""

        return render_to_string(self.template, {"formset": self.formset_in_context})

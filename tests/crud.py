"""CRUD module"""
from vega_admin.views import VegaCRUDView

from tiny_erp.apps.purchases.forms import RequisitionForm
from tiny_erp.apps.purchases.models import Requisition


class RequisitionCRUD(VegaCRUDView):
    """
    CRUD view for Requisitions
    """

    model = Requisition
    protected_actions = None
    permissions_actions = None
    form_class = RequisitionForm


urlpatterns = RequisitionCRUD().url_patterns()

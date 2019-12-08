"""CRUD module"""
from vega_admin.views import VegaCRUDView

from tiny_erp.apps.purchases.forms import (
    RequisitionForm,
    RequisitionProductForm,
    UpdatedRequisitionProductForm,
    UpdateRequisitionForm,
)
from tiny_erp.apps.purchases.models import Requisition


class RequisitionCRUD(VegaCRUDView):
    """
    CRUD view for Requisitions
    """

    model = Requisition
    protected_actions = None
    permissions_actions = None
    form_class = RequisitionForm
    create_form_class = RequisitionForm
    update_form_class = UpdateRequisitionForm


class RequisitionProductCRUD(VegaCRUDView):
    """
    CRUD view for Requisitions
    """

    model = Requisition
    protected_actions = None
    permissions_actions = None
    form_class = RequisitionProductForm
    create_form_class = RequisitionProductForm
    update_form_class = UpdatedRequisitionProductForm
    crud_path = "req-products"


urlpatterns = RequisitionCRUD().url_patterns() + RequisitionProductCRUD().url_patterns()

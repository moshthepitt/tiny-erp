"""Configurable options."""
from django.conf import settings

TINY_ERP_DEFAULT_CURRENCY = "KES"
TINY_ERP_AVAILABLE_CURRENCIES = [("KES", "Kenya Shilling")]

# strings
TINY_ERP_REQUISITION_ITEMS_TXT = "Requisition Items"
TINY_ERP_SUBMIT_TXT = "Submit"
TINY_ERP_REQUISITION_FORMSET_ERROR_TXT = (
    "There is an error in the requisition line items."
)
# emails
TINY_ERP_ADMIN_NAME = "ERP"
TINY_ERP_ADMIN_EMAILS = [settings.DEFAULT_FROM_EMAIL]
TINY_ERP_ACCOUNTS_EMAILS = [settings.DEFAULT_FROM_EMAIL]
# TINY_ERP_REQUISITION_FILED_EMAIL_TXT - body of requisition filed email
# TINY_ERP_REQUISITION_FILED_EMAIL_SUBJ - subject of requisition filed email
# TINY_ERP_REQUISITION_UPDATED_EMAIL_TXT - body of requisition updated email
# TINY_ERP_REQUISITION_UPDATED_EMAIL_SUBJ - - subject of requisition updated email
# TINY_ERP_REQUISITION_APPROVED_EMAIL_TXT - body of requisition updated email
# TINY_ERP_REQUISITION_APPROVED_EMAIL_SUBJ - - subject of requisition updated email

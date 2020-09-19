"""Configurable options."""
from typing import List

from django.conf import settings

TINY_ERP_DEFAULT_CURRENCY = "KES"
TINY_ERP_AVAILABLE_CURRENCIES = [("KES", "Kenya Shilling")]
# emails
TINY_ERP_ADMIN_NAME = "ERP"
# list of email addresses to review purchase requisitions
TINY_ERP_REQUISITION_REVIEWERS: List[str] = []
# If true we will have tiered levels of review i.e. TINY_ERP_REQUISITION_REVIEWERS[0]
# must approve before TINY_ERP_REQUISITION_REVIEWERS[1] gets notified etc.
TINY_ERP_REQUISITION_REVIEWS_TIERS: bool = False
TINY_ERP_ADMIN_EMAILS = [settings.DEFAULT_FROM_EMAIL]  # should remove?
TINY_ERP_ACCOUNTS_EMAILS = [settings.DEFAULT_FROM_EMAIL]  # should remove?

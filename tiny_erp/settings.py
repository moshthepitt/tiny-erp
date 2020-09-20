"""Configurable options."""
from typing import List, Optional

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

# path to function that will be used to determine the user for a review object
TINY_ERP_REQUISITION_SET_USER_FUNCTION: Optional[str] = None
# path to function that will be used to determine reviewers
TINY_ERP_REQUISITION_SET_REVIEWERS_FUNCTION: Optional[str] = None
# path to function that will be used to send email to reviewers
TINY_ERP_REQUISITION_REQUEST_FOR_REVIEW_FUNCTION: Optional[str] = None
# path to function that will be used to determine reviewers
TINY_ERP_REQUISITION_GET_NEXT_REVIEWERS: Optional[str] = None

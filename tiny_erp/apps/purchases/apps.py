"""
Apps module for purchases app
"""
from django.apps import AppConfig


class PurchasesConfig(AppConfig):
    """
    Apps config class
    """

    name = "purchases"
    app_label = "tiny_erp"

    def ready(self):
        # set up app settings
        from tiny_erp.anza import setup_settings  # noqa
        setup_settings()

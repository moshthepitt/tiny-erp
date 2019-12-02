"""
Apps module for purchases app
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PurchasesConfig(AppConfig):
    """
    Apps config class
    """

    name = "tiny_erp.apps.purchases"
    app_label = "tiny_erp"
    verbose_name = _("Purchases")

    def ready(self):
        # set up app settings
        # pylint: disable=import-outside-toplevel
        from tiny_erp.anza import setup_settings  # noqa

        setup_settings()

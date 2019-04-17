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
        from django.conf import settings
        import tiny_erp.settings as defaults

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))

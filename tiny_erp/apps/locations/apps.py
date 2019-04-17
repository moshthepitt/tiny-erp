"""
Apps module for locations app
"""
from django.apps import AppConfig


class LocationsConfig(AppConfig):
    """
    Apps config class
    """

    name = "locations"
    app_label = "tiny_erp"

    def ready(self):
        # set up app settings
        from tiny_erp.anza import setup_settings  # noqa
        setup_settings()

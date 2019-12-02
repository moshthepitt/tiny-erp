"""
Apps module for locations app
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LocationsConfig(AppConfig):
    """
    Apps config class
    """

    name = "tiny_erp.apps.locations"
    app_label = "tiny_erp"
    verbose_name = _("Locations")

    def ready(self):
        # set up app settings
        # pylint: disable=import-outside-toplevel
        from tiny_erp.anza import setup_settings  # noqa

        setup_settings()

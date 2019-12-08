"""Apps module for products app."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProductsConfig(AppConfig):
    """Apps config class."""

    name = "tiny_erp.apps.products"
    app_label = "tiny_erp"
    verbose_name = _("products")

    def ready(self):
        # set up app settings
        # pylint: disable=import-outside-toplevel
        from tiny_erp.anza import setup_settings  # noqa

        setup_settings()

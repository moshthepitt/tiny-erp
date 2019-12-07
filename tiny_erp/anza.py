"""module to handle things that are done to setup tiny_erp."""


def setup_settings():
    """Set up app settings."""
    # pylint: disable=import-outside-toplevel
    from django.conf import settings
    import tiny_erp.settings as defaults

    for name in dir(defaults):
        if name.isupper() and not hasattr(settings, name):
            setattr(settings, name, getattr(defaults, name))

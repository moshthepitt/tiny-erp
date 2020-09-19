"""widgets module."""
from django.forms.widgets import Textarea


class MiniTextarea(Textarea):
    """Vertically shorter version of textarea widget."""

    rows = 2

    def __init__(self, attrs=None):
        """Initialize."""
        super().__init__({"rows": self.rows})

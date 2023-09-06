"""
This config file is kept for backwards compatibility, almost all the config has
now been moved into the theme itself or can be imported from the main namespace
of the theme.
"""
from sunpy_sphinx_theme import ON_RTD as on_rtd  # noqa
from sunpy_sphinx_theme import PNG_ICON as png_icon  # noqa
from sunpy_sphinx_theme import SVG_ICON as svg_icon  # noqa

__all__ = ["html_theme", "on_rtd", "png_icon", "svg_icon"]

html_theme = "sunpy"
html_theme_options = {}

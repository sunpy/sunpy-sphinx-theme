import os

from sunpy_sphinx_theme import get_html_theme_path

html_theme = "sunpy"

_sunpy_theme_path = get_html_theme_path()
_sunpy_static_path = _sunpy_theme_path / "static"
svg_icon = _sunpy_static_path / "img" / "sunpy_icon.svg"
png_icon = _sunpy_static_path / "img" / "sunpy_icon_128x128.png"
on_rtd = os.environ.get("READTHEDOCS", False) == "True"

html_theme_options = {}

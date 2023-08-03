import os

from sunpy_sphinx_theme import get_html_theme_path

html_theme = "sunpy"

html_theme_path = get_html_theme_path()
html_static_path = [os.path.join(html_theme_path[0], html_theme, "static")]
svg_icon = os.path.join(html_static_path[0], "img", "sunpy_icon.svg")
png_icon = os.path.join(html_static_path[0], "img", "sunpy_icon_128x128.png")
on_rtd = os.environ.get("READTHEDOCS", False) == "True"

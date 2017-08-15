import os
from urllib.parse import urljoin
from . import get_html_theme_path

html_theme_path = get_html_theme_path()
html_theme = "sunpy"
html_favicon = os.path.join(html_theme_path[0], html_theme, "static", "img", "favicon-32.ico")

def page_url(page):
    sunpy_website_url_base = "http://sunpy.org/"
    return urljoin(sunpy_website_url_base, page)

html_theme_options = {
    'navbar_links': [
        ("Support Us", page_url("contribute.html"), 1),
        ("Get Help", page_url("help.html"), 1),
        ("SunPy Project", page_url("team.html"), 1),
    ]
}

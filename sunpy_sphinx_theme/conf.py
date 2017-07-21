import os
from urllib.parse import urljoin
from . import get_html_theme_path

html_theme_path = get_html_theme_path()

html_theme = "sunpy"

def page_url(page):
    sunpy_website_url_base = "https://duygukeskek.github.io/sunpy-website/"
    return urljoin(sunpy_website_url_base, page)


html_theme_options = {
    'navbar_links': [
        ("About", page_url("about.html"), 1),
        ("Blog", page_url("blog.html"), 1),
        ("Documentation", "http://sunpy.org/sunpy-sphinx-theme/index"),
        ("Support Us", page_url("contribute.html"), 1),
        ("Get Help", page_url("help.html"), 1),
        ("SunPy Project", page_url("team.html"), 1),
    ]
}

html_favicon = os.path.join(html_theme_path[0], html_theme, "static", "img",
														"favicon-32.ico")

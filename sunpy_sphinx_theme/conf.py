import os
try:
    from urllib.parse import urljoin, urlparse
except ImportError:
    from urlparse import urljoin, urlparse

from sunpy_sphinx_theme import get_html_theme_path

html_theme_path = get_html_theme_path()
html_theme = "sunpy"
html_static_path = [os.path.join(html_theme_path[0], html_theme, "static")]
html_favicon = os.path.join(html_static_path[0], "img", "favicon-32.ico")


def page_url(page):
    sunpy_website_url_base = "http://sunpy.org/"
    return urljoin(sunpy_website_url_base, page)


html_sidebars = {'**': ['docsidebar.html']}
html_theme_options = {
    'navbar_links': [
        ("About", page_url("about.html"), 1),
        ("Blog", page_url("blog.html"), 1),
        ("Support Us", page_url("contribute.html"), 1),
        ("Get Help", page_url("help.html"), 1),
        ("SunPy Project", page_url("team.html"), 1)
                    ]
}

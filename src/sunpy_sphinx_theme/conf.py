import os
import socket
from urllib.parse import urljoin

from sunpy_sphinx_theme import get_html_theme_path


def page_url(page):
    """
    Gets the formal URL for a page.

    Parameters
    ----------
    page : `str`
        HTML file/page name

    Returns
    -------
    `str`
        The URL for the page.
    """
    return urljoin(sunpy_website_url_base, page)


html_theme = "sunpy"
theme_base_path = get_html_theme_path()
img_dir = theme_base_path / "static" / "images"
html_favicon = str(img_dir / "favicon-32.ico")
html_logo = png_icon = str(img_dir / "sunpy_icon_128x128.png")
svg_icon = str(img_dir / "sunpy_icon.svg")

on_rtd = os.environ.get("READTHEDOCS", False) == "True"
if on_rtd:
    sunpy_website_url_base = "https://sunpy.org"
else:
    sunpy_website_url_base = socket.gethostname()

html_theme_options = {
    "page_toctree_depths": {"generated/gallery": 2},
    "on_rtd": on_rtd,
    "header": {
        "brand": {
            "type": "text",
            "content": "SunPy",
            "url": "https://sunpy.org",
        },
        "start": [
            {
                "type": "dropdown",
                "content": "About",
                "items": [
                    {"url": page_url("about.html"), "content": "Our Mission"},
                    {"url": page_url("about.html") + "#acknowledging-or-citing-sunpy", "content": "Acknowledge SunPy"},
                    {"url": page_url("coc.html"), "content": "Code of Conduct"},
                ],
            },
            {
                "type": "dropdown",
                "content": "Documentation",
                "items": [
                    {"url": "https://docs.sunpy.org", "content": "sunpy"},
                    {"url": "https://docs.sunpy.org/projects/ndcube/", "content": "ndcube"},
                    {"url": "https://docs.sunpy.org/projects/drms/", "content": "drms"},
                    {"url": "https://aiapy.readthedocs.io", "content": "aiapy"},
                    {"url": "https://pfsspy.readthedocs.io", "content": "pfsspy"},
                    {"url": "https://docs.sunpy.org/projects/sunraster", "content": "sunraster"},
                    {"url": "https://docs.sunpy.org/projects/sunkit-instruments", "content": "sunkit-instruments"},
                    {"url": "https://docs.sunpy.org/projects/sunkit-image", "content": "sunkit-image"},
                    {"url": "https://docs.sunpy.org/projects/radiospectra", "content": "radiospectra"},
                    {"url": "https://pyflct.readthedocs.io", "content": "pyflct"},
                    {"url": "https://ablog.readthedocs.io", "content": "ablog"},
                ],
            },
            {"type": "text", "url": page_url("blog.html"), "content": "Blog"},
            {"type": "text", "url": page_url("contribute.html"), "content": "Support Us"},
            {"type": "text", "url": page_url("help.html"), "content": "Get Help"},
            {
                "type": "dropdown",
                "content": "SunPy Project",
                "items": [
                    {"url": page_url("project/"), "content": "SunPy Project"},
                    {"url": page_url("project/roles.html"), "content": "Community Roles"},
                    {"url": page_url("project/affiliated.html"), "content": "Affiliated Packages"},
                    {"url": page_url("project/former.html"), "content": "Emeritus role holders"},
                    {"url": page_url("project/meetings.html"), "content": "Meetings"},
                ],
            },
        ],
    },
    # Only really setup to look nice with 3 links.
    "footer_links": [
        ("GitHub", "https://github.com/sunpy", 1),
        ("Twitter", "https://twitter.com/SunPyProject", 1),
        ("Chat", "https://openastronomy.element.io/#/room/#sunpy:openastronomy.org", 1),
    ],
}

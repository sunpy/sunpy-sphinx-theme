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

img_dir = theme_base_path / "static" / "img"
html_favicon = str(img_dir / "favicon-32.ico")
html_logo = png_icon = str(img_dir / "sunpy_icon_128x128.png")
svg_icon = str(img_dir / "sunpy_icon.svg")


on_rtd = os.environ.get("READTHEDOCS", False) == "True"
if on_rtd:
    sunpy_website_url_base = "https://sunpy.org"
else:
    sunpy_website_url_base = socket.gethostname()

html_sidebars = {
    "**": ["docsidebar.html"],
}
html_theme_options = {
    "page_toctree_depths": {"generated/gallery": 2},
    "on_rtd": on_rtd,
    "navbar_links": [
        (
            "About",
            [
                ("Our Mission", page_url("about.html"), 1),
                (
                    "Acknowledge SunPy",
                    page_url("about.html") + "#acknowledging-or-citing-sunpy",
                    1,
                ),
                (
                    "Code of Conduct",
                    page_url("coc.html"),
                    1,
                ),
            ],
            1,
        ),
        (
            "Documentation",
            [
                ("sunpy", "https://docs.sunpy.org/en/stable/", 1),
                ("ndcube", "https://docs.sunpy.org/projects/ndcube/", 1),
                ("drms", "https://docs.sunpy.org/projects/drms/", 1),
                ("aiapy", "https://aiapy.readthedocs.io/en/stable/", 1),
                ("pfsspy", "https://pfsspy.readthedocs.io/en/stable/", 1),
                (
                    "sunraster",
                    "https://docs.sunpy.org/projects/sunraster/en/stable/",
                    1,
                ),
                (
                    "sunkit-instruments",
                    "https://docs.sunpy.org/projects/sunkit-instruments/en/stable/",
                    1,
                ),
                (
                    "sunkit-image",
                    "https://docs.sunpy.org/projects/sunkit-image/en/stable/",
                    1,
                ),
                (
                    "radiospectra",
                    "https://docs.sunpy.org/projects/radiospectra/en/stable/",
                    1,
                ),
                ("pyflct", "https://pyflct.readthedocs.io/en/stable/", 1),
                ("ablog", "https://ablog.readthedocs.io/", 1),
            ],
            1,
        ),
        ("Blog", page_url("blog.html"), 1),
        ("Support Us", page_url("contribute.html"), 1),
        ("Get Help", page_url("help.html"), 1),
        (
            "SunPy Project",
            [
                ("SunPy Project", page_url("project/"), 1),
                (
                    "Community Roles",
                    page_url("project/roles.html"),
                    1,
                ),
                (
                    "Affiliated Packages",
                    page_url("project/affiliated.html"),
                    1,
                ),
                (
                    "Emeritus role holders",
                    page_url("project/former.html"),
                    1,
                ),
                (
                    "Meetings",
                    page_url("project/meetings.html"),
                    1,
                ),
            ],
            1,
        ),
    ],
    # Only really setup to look nice with 3 values.
    "footer_links": [
        ("GitHub", "https://github.com/sunpy/sunpy", 1),
        ("Twitter", "https://twitter.com/SunPyProject", 1),
        ("Matrix", "https://app.element.io/#/room/#sunpy:openastronomy.org", 1),
    ],
}

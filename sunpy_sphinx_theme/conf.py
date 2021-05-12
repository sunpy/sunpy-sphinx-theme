import os
import socket
from urllib.parse import urljoin

from sunpy_sphinx_theme import get_html_theme_path

html_theme_path = get_html_theme_path()
html_theme = "sunpy"
html_static_path = [os.path.join(html_theme_path[0], html_theme, "static")]
html_extra_path = [os.path.join(html_theme_path[0], html_theme, "static", "img")]
templates_path = [os.path.join(html_theme_path[0], html_theme, "templates")]
html_favicon = os.path.join(html_static_path[0], "img", "favicon-32.ico")
svg_icon = os.path.join(html_static_path[0], "img", "sunpy_icon.svg")

on_rtd = os.environ.get("READTHEDOCS", False) == "True"

if on_rtd:
    sunpy_website_url_base = "https://sunpy.org"
else:
    sunpy_website_url_base = socket.gethostname()


def page_url(page):
    return urljoin(sunpy_website_url_base, page)


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
                ("sunraster", "https://docs.sunpy.org/projects/sunraster/en/stable/", 1),
                ("sunkit-instruments", "https://docs.sunpy.org/projects/sunkit-instruments/en/stable/", 1),
                ("sunkit-image", "https://docs.sunpy.org/projects/sunkit-image/en/stable/", 1),
                ("radiospectra", "https://docs.sunpy.org/projects/radiospectra/en/stable/", 1),
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
                ("Community Roles", page_url("project/roles.html"), 1),
                ("Affiliated Packages", page_url("project/affiliated.html"), 1),
                ("Emeritus role holders", page_url("project/former.html"), 1),
            ],
            1,
        ),
    ],
    # Only really setup to look nice with 3 values.
    "footer_links": [
        ("Github", "https://github.com/sunpy/sunpy", 1),
        ("Twitter", "https://twitter.com/SunPyProject", 1),
        ("Matrix", "https://app.element.io/#/room/#sunpy:openastronomy.org", 1),
    ],
}


def fix_circleci(app):
    # Circle CI does weird things with redirections, which seem to break the
    # import statements in the css files in the bootstrap theme. By doing this
    # here we include these css files which are normally imported directly in
    # the html which means they redirect properly. We only need to do this on
    # circleci.
    print(f"Checking for circleci: {os.environ.get('CIRCLECI')}")
    if os.environ.get("CIRCLECI"):
        app.add_css_file("basic.css")
        app.add_css_file("bootswatch-3.3.7/flatly/bootstrap.min.css")


def setup(app):
    fix_circleci(app)

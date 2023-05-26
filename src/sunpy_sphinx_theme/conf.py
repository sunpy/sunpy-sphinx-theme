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
png_icon = os.path.join(html_static_path[0], "img", "sunpy_icon_128x128.png")
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
                ("Our Mission", page_url("about/mission.html"), 1),
                ("The SunPy Project", page_url("about/project.html"), 1),
                ("Community Roles", page_url("about/roles.html"), 1),
                ("Meetings", page_url("about/meetings.html"), 1),
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
                ("sunpy", "https://docs.sunpy.org/", 1),
                ("ndcube", "https://docs.sunpy.org/projects/ndcube/", 1),
                ("aiapy", "https://aiapy.readthedocs.io/", 1),
                ("drms", "https://docs.sunpy.org/projects/drms/", 1),
                ("pfsspy", "https://pfsspy.readthedocs.io/", 1),
                ("radiospectra", "https://docs.sunpy.org/projects/radiospectra/", 1),
                ("sunkit-instruments ", "https://docs.sunpy.org/projects/sunkit-instruments/", 1),
                ("sunkit-image", "https://docs.sunpy.org/projects/sunkit-image/", 1),
                ("sunraster", "https://docs.sunpy.org/projects/sunraster/", 1),
                ("sunpy-soar", "https://github.com/sunpy/sunpy-soar#readme", 1),
                ("roentgen", "https://roentgen.readthedocs.io/", 1),
            ],
            1,
        ),
        ("Affiliated Packages", page_url("affiliated.html"), 1),
        ("Get Help", page_url("help.html"), 1),
        ("Contribute", page_url("contribute.html"), 1),
        ("Blog", page_url("blog.html"), 1),
    ],
    # Only really setup to look nice with 3 values.
    "footer_links": [
        ("GitHub", "https://github.com/sunpy", 1),
        ("Twitter", "https://twitter.com/SunPyProject", 1),
        ("Chat", "https://openastronomy.element.io/#/room/#sunpy:openastronomy.org", 1),
    ],
}

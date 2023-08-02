"""
SunPy Sphinx Theme.
"""
import os
import socket
from pathlib import Path
from urllib.parse import urljoin

from pydata_sphinx_theme import utils
from sphinx.application import Sphinx

ON_RTD = os.environ.get("READTHEDOCS", False) == "True"


def get_html_theme_path():
    """
    Return list of HTML theme paths.
    """
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "sunpy"
    return theme_path


def page_url(page):
    if ON_RTD:
        sunpy_website_url_base = "https://sunpy.org"
    else:
        sunpy_website_url_base = socket.gethostname()
    return urljoin(sunpy_website_url_base, page)


def default_navbar():
    return [
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
                ("sunpy", page_url("/"), 1),
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
    ]


def update_config(app):
    """
    Update config with new default values and handle deprecated keys.
    """
    # By the time `builder-inited` happens, `app.builder.theme_options` already exists.
    # At this point, modifying app.config.html_theme_options will NOT update the
    # page's HTML context (e.g. in jinja, `theme_keyword`).
    # To do this, you must manually modify `app.builder.theme_options`.
    theme_options = utils.get_theme_options_dict(app)

    if not theme_options.get("navbar_links"):
        theme_options["navbar_links"] = default_navbar()

    if not theme_options.get("footer_start"):
        theme_options["footer_start"] = ["templates/page-footer.html"]

    if not theme_options.get("footer_links"):
        theme_options["footer_links"] = [
            ("GitHub", "https://github.com/sunpy", 1),
            ("Discourse", "https://community.openastronomy.org/c/sunpy", 1),
            ("Chat", "https://openastronomy.element.io/#/room/#sunpy:openastronomy.org", 1),
        ]


def setup(app: Sphinx):
    # Register theme
    theme_dir = get_html_theme_path()
    app.add_html_theme("sunpy", theme_dir)
    app.add_css_file("sunpy_style.css")

    app.connect("builder-inited", update_config)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

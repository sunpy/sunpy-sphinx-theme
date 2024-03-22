"""
SunPy Sphinx Theme.
"""

import os
from pathlib import Path
from functools import partial
from urllib.parse import urljoin

from pydata_sphinx_theme import utils
from sphinx.application import Sphinx

__all__ = ["get_html_theme_path", "ON_RTD", "PNG_ICON", "SVG_ICON"]


def get_html_theme_path():
    """
    Return list of HTML theme paths.
    """
    parent = Path(__file__).parent.resolve()
    return parent / "theme" / "sunpy"


def default_navbar():
    return [
        (
            "About",
            [
                ("Our Mission", "about/index.html", 2),
                ("SunPy Project", "about/project.html", 2),
                ("Presentations", "about/presentations.html", 2),
                ("Community Roles", "about/roles.html", 2),
                ("Meetings", "about/meetings.html", 2),
                ("Code of Conduct", "coc.html", 2),
            ],
        ),
        (
            "Documentation",
            [
                ("sunpy", "https://docs.sunpy.org/", 3),
                ("ndcube", "https://docs.sunpy.org/projects/ndcube/", 3),
                ("aiapy", "https://aiapy.readthedocs.io/", 3),
                ("drms", "https://docs.sunpy.org/projects/drms/", 3),
                ("pfsspy", "https://pfsspy.readthedocs.io/", 3),
                ("radiospectra", "https://docs.sunpy.org/projects/radiospectra/", 3),
                ("sunkit-instruments ", "https://docs.sunpy.org/projects/sunkit-instruments/", 3),
                ("sunkit-image", "https://docs.sunpy.org/projects/sunkit-image/", 3),
                ("sunraster", "https://docs.sunpy.org/projects/sunraster/", 3),
                ("sunpy-soar", "https://github.com/sunpy/sunpy-soar#readme", 3),
                ("roentgen", "https://roentgen.readthedocs.io/", 3),
                ("demcmc", "https://demcmc.readthedocs.io/en/latest/", 3),
                ("dkist", "https://docs.dkist.nso.edu/projects/python-tools", 3),
            ],
        ),
        ("Affiliated Packages", "affiliated.html", 2),
        ("Get Help", "help.html", 2),
        ("Contribute", "contribute.html", 2),
        ("Blog", "blog.html", 2),
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

    if theme_options.get("sst_logo") and not isinstance(theme_options["sst_logo"], dict):
        sst_logo = str(theme_options["sst_logo"])
        theme_options["sst_logo"] = {"light": sst_logo, "dark": sst_logo}

    theme_options["sst_is_root"] = bool(theme_options.get("sst_is_root", False))

    if not theme_options.get("navbar_links"):
        theme_options["navbar_links"] = default_navbar()

    if not theme_options.get("footer_links", False):
        theme_options["footer_links"] = [
            ("Code", "https://github.com/sunpy", 3),
            ("Forum", "https://community.openastronomy.org/c/sunpy", 3),
            ("Chat", "https://openastronomy.element.io/#/room/#sunpy:openastronomy.org", 3),
        ]

    # TODO: This is nasty
    # Set the default value of show_source to False unless it's specified in the user config
    if "html_show_sourcelink" not in app.config._raw_config:
        app.config.html_show_sourcelink = False

    # Set the logo to the sunpy logo unless it's overridden in the user config
    if "html_logo" not in app.config._raw_config:
        app.config.html_logo = str(get_html_theme_path() / "static" / "img" / "sunpy_icon.svg")


def sst_pathto(context, document, relative_to=0):
    """
    This is a modified version of the built-in ``pathto()`` function.

    The default version when called with one argument returns the URL to a
    sphinx document, when specified with a 1 as the second argument it returns
    the path to a file relative to the root of the generated output.

    This version has 4 modes:
    * ``sst_pathto(document)`` - The same as ``pathto(document)``
    * ``sst_pathto(document, 1)`` - The same as ``pathto(document, 1)``
    * ``sst_pathto(document, 2)`` - A URL relative to ``sst_site_root`` will be returned when ``sst_is_root`` is ``False`` and the equivalent of specifying 1 as the second argument when it is ``True``.
    * ``sst_pathto(document, 3)`` - Do nothing return ``document`` unmodified.
    """
    if relative_to == 0:
        return context["pathto"](document)
    elif relative_to == 1:
        return context["pathto"](document, 1)
    elif relative_to == 2:
        if context.get("theme_sst_is_root", False):
            return context["pathto"](document, 1)
        return urljoin(context["theme_sst_site_root"], document)
    elif relative_to == 3:
        return document
    else:
        raise ValueError("The third element of a link tuple must be 1, 2 or 3")


def update_html_context(app: Sphinx, pagename: str, templatename: str, context, doctree) -> None:
    """
    Set extra things to use in jinja templates.
    """
    context["favicon_url"] = context.get("favicon_url", None) or "_static/img/sunpy_icon.svg"
    context["sst_pathto"] = partial(sst_pathto, context)


def setup(app: Sphinx):
    # Register theme
    theme_dir = get_html_theme_path()
    app.add_html_theme("sunpy", theme_dir)
    app.add_css_file("sunpy_style.css", priority=600)

    app.connect("builder-inited", update_config)
    app.connect("html-page-context", update_html_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


_sunpy_static_path = get_html_theme_path() / "static"
ON_RTD = os.environ.get("READTHEDOCS", False) == "True"
SVG_ICON = _sunpy_static_path / "img" / "sunpy_icon.svg"
PNG_ICON = _sunpy_static_path / "img" / "sunpy_icon_128x128.png"

"""
SunPy Sphinx Theme.
"""

import os
from functools import partial
from pathlib import Path
from urllib.parse import urljoin

from pydata_sphinx_theme import utils
from sphinx.application import Sphinx

__all__ = ["ON_RTD", "PNG_ICON", "SVG_ICON", "get_html_theme_path"]


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
                ("Our Mission", "about/", 2),
                ("SunPy Project", "about/project/", 2),
                ("Presentations", "about/presentations/", 2),
                ("Meetings", "about/meetings/", 2),
                ("Code of Conduct", "coc/", 2),
            ],
        ),
        (
            "Documentation",
            [
                # Core goes first always
                ("sunpy", "https://docs.sunpy.org/", 3),
                # Other affiliated packages are in alphabetical order
                ("aiapy", "https://aiapy.readthedocs.io/", 3),
                ("dkist", "https://docs.dkist.nso.edu/projects/python-tools", 3),
                ("drms", "https://docs.sunpy.org/projects/drms/", 3),
                ("irispy-lmsal", "https://irispy-lmsal.readthedocs.io/", 3),
                ("ndcube", "https://docs.sunpy.org/projects/ndcube/", 3),
                ("roentgen", "https://roentgen.readthedocs.io/", 3),
                ("solarmach", "https://solarmach.readthedocs.io/en/stable/", 3),
                ("sunkit-image", "https://docs.sunpy.org/projects/sunkit-image/", 3),
                ("sunkit-instruments ", "https://docs.sunpy.org/projects/sunkit-instruments/", 3),
                ("sunkit-magex", "https://docs.sunpy.org/projects/sunkit-magex/", 3),
                ("sunkit-pyvista", "https://docs.sunpy.org/projects/sunkit-pyvista/", 3),
                ("sunpy-soar", "https://docs.sunpy.org/projects/soar/", 3),
                ("sunraster", "https://docs.sunpy.org/projects/sunraster/", 3),
                ("xrtpy", "https://xrtpy.readthedocs.io/", 3),
                # Provisional packages submenu
                (
                    "Provisional",
                    [
                        ("pyflct", "https://pyflct.readthedocs.io/", 3),
                        ("radiospectra", "https://docs.sunpy.org/projects/radiospectra/", 3),
                    ],
                ),
                # Tools submenu
                (
                    "Tools",
                    [
                        ("ablog", "https://ablog.readthedocs.io/en/stable/", 3),
                        ("mpl-animators", "https://docs.sunpy.org/projects/mpl-animators/", 3),
                        ("streamtracer", "https://docs.sunpy.org/projects/streamtracer/", 3),
                    ],
                ),
            ],
        ),
        ("Packages", "affiliated/", 2),
        ("Get Help", "help/", 2),
        ("Contribute", "contribute/", 2),
        ("Blog", "blog/", 2),
        ("Cite SunPy", "https://docs.sunpy.org/en/stable/citation.html", 3),
    ]


def update_config(app) -> None:
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
    if "html_show_sourcelink" not in app.config._raw_config:  # NOQA: SLF001
        app.config.html_show_sourcelink = False

    # Set the logo to the sunpy logo unless it's overridden in the user config
    if "html_logo" not in app.config._raw_config:  # NOQA: SLF001
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
    elif relative_to == 1:  # NOQA: RET505
        return context["pathto"](document, 1)
    elif relative_to == 2:
        if context.get("theme_sst_is_root", False):
            return context["pathto"](document, 1)
        return urljoin(context["theme_sst_site_root"], document)
    elif relative_to == 3:
        return document
    else:
        msg = "The third element of a link tuple must be 1, 2 or 3"
        raise ValueError(msg)


def update_html_context(app: Sphinx, pagename: str, templatename: str, context, doctree) -> None:  # NOQA: ARG001
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
    # Conditionally include goat counter js
    # We can't do this in update_config as that causes the scripts to be duplicated.
    # Also in here none of the theme defaults have be applied by `update_config`
    # TODO: Improve this mess
    theme_options = utils.get_theme_options_dict(app)
    # We want to default to the sunpy goat counter only if the sst_site_root is sunpy.org
    root_domain = theme_options.get("sst_site_root", "https://sunpy.org")
    sunpy_goat_url = "https://sunpy.goatcounter.com/count"
    default_goat_url = sunpy_goat_url if root_domain == "https://sunpy.org" else None
    if primary_goat_url := theme_options.get("goatcounter_analytics_url", default_goat_url):
        root_domain = root_domain.removeprefix("https://").removeprefix("http://")
        default_endpoint = theme_options.get("goatcounter_non_domain_endpoint", False)
        if default_endpoint is False:
            default_endpoint = ""
        app.add_js_file(
            None,
            body=f"""
            var endpoint = '{default_endpoint}';
            if (location.hostname.endsWith('{root_domain}')) {{
                endpoint = '{primary_goat_url}'
            }}

            window.goatcounter = {{
                endpoint: endpoint,
                path: function(p) {{ return location.host + p }}
            }}
            """,
        )
        app.add_js_file(
            "https://gc.zgo.at/count.js",
            loading_method="async",
        )
        app.add_js_file(
            "js/submenu-concertina-toggle.js",
            loading_method="async",
        )

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


_sunpy_static_path = get_html_theme_path() / "static"
ON_RTD = os.environ.get("READTHEDOCS", "False") == "True"
SVG_ICON = _sunpy_static_path / "img" / "sunpy_icon.svg"
PNG_ICON = _sunpy_static_path / "img" / "sunpy_icon_128x128.png"

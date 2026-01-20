"""
SunPy Sphinx Theme.
"""

import json
import os
from functools import partial
from pathlib import Path
from textwrap import dedent, indent
from urllib.parse import urljoin

from pydata_sphinx_theme import utils
from sphinx.application import Sphinx

__all__ = ["ON_RTD", "PNG_ICON", "SVG_ICON", "get_html_theme_path"]


def get_theme_options(app):
    """
    This gets the user configured options and the defaults and merges them.
    """
    return {**app.builder.theme.get_options(), **utils.get_theme_options_dict(app)}


def get_html_theme_path():
    """
    Return list of HTML theme paths.
    """
    parent = Path(__file__).parent.resolve()
    return parent / "theme" / "sunpy"


def update_config(app) -> None:
    """
    Update config with new default values and handle deprecated keys.
    """
    # By the time `builder-inited` happens, `app.builder.theme_options` already exists.
    # At this point, modifying app.config.html_theme_options will NOT update the
    # page's HTML context (e.g. in jinja, `theme_keyword`).
    # To do this, you must manually modify `app.builder.theme_options`.
    theme_options_with_defaults = get_theme_options(app)
    theme_options = utils.get_theme_options_dict(app)

    if theme_options_with_defaults.get("sst_logo") and not isinstance(theme_options_with_defaults["sst_logo"], dict):
        sst_logo = str(theme_options["sst_logo"])
        theme_options["sst_logo"] = {"light": sst_logo, "dark": sst_logo}

    theme_options["sst_is_root"] = bool(theme_options_with_defaults.get("sst_is_root", False))

    # Set the default value of show_source to False unless it's specified in the user config
    if not utils.config_provided_by_user(app, "html_show_sourcelink"):
        app.config.html_show_sourcelink = False

    # Set the logo to the sunpy logo unless it's overridden in the user config
    if not utils.config_provided_by_user(app, "html_logo"):
        app.config.html_logo = str(get_html_theme_path() / "static" / "img" / "sunpy_icon.svg")

    # Include sunpy.org in extra_search_projects as long as none of
    # navbar_links, rtd_search_projects and rtd_extra_search_projects
    # are set, i.e. you are using the default sunpy set of projects.
    # Without this non-sunpy projects would have to explicitly un-set
    # rtd_extra_search_projects
    if not (
        utils.config_provided_by_user(app, "navbar_links")
        or utils.config_provided_by_user(app, "rtd_search_projects")
        or utils.config_provided_by_user(app, "rtd_extra_search_projects")
    ):
        theme_options["rtd_extra_search_projects"] = [["sunpyorg", "https://sunpy.org"]]


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


def generate_search_config(app):
    """
    This function parses the config for the "Documentation" section of the theme config.
    """
    theme_config = get_theme_options(app)
    search_projects = theme_config.get("rtd_search_projects", None)
    if not search_projects:
        navbar_links = theme_config["navbar_links"]
        doc_links = next(section[1] for section in navbar_links if section[0] == "Documentation")

        def filter_doc_links(links):
            out_links = []
            for link in links:
                if isinstance(link[1], list):
                    out_links += filter_doc_links(link[1])
                elif isinstance(link[1], str) and link[1].startswith("http"):
                    out_links.append({"name": link[0], "link": link[1]})
                else:
                    err = f"Unable to parse {link} in the nav tree. Try setting search_projects explicitly or fixing navbar_links."
                    raise ValueError(err)
            return out_links

        search_projects = filter_doc_links(doc_links)

    if extra_search_projects := theme_config.get("rtd_extra_search_projects", None):
        search_projects += filter_doc_links(extra_search_projects)

    load_more_label = theme_config.get("rtd_search_load_more_label", "Load more results")
    no_results_label = theme_config.get("rtd_search_no_results_label", "There are no results for this search")
    script = dedent(f"""
        const set_search_config = {{
          "no-results":{{
            "label": "{no_results_label}"
          }},
          "load-more":{{
            "label": "{load_more_label}",
            "class": "btn sd-btn sd-bg-primary sd-bg-text-primary"
          }},
          "projects":{indent(json.dumps(search_projects, indent=2), " " * 10, predicate=lambda line: line.strip() != "[")}
        }};
    """)
    app.add_js_file(None, body=script)


def setup(app: Sphinx):
    # Register theme
    theme_dir = get_html_theme_path()
    app.add_html_theme("sunpy", theme_dir)
    app.add_css_file("sunpy_style.css", priority=600)
    app.connect("builder-inited", update_config, priority=100)
    app.connect("builder-inited", generate_search_config, priority=500)
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

        if theme_options.get("rtd_search", True):
            # Add project-wide search
            app.add_css_file("css/rtd_enhanced_search.css")
            app.add_js_file(
                "js/rtd_enhanced_search.js",
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

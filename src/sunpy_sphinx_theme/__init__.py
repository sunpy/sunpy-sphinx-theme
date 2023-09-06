"""
SunPy Sphinx Theme.
"""
import os
from pathlib import Path
from functools import partial
from urllib.parse import urljoin

from pydata_sphinx_theme import utils
from sphinx.application import Sphinx


def get_html_theme_path():
    """
    Return list of HTML theme paths.
    """
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "theme" / "sunpy"
    return theme_path


def default_navbar(path_to):
    return [
        (
            "About",
            [
                ("Our Mission", path_to("about/index"), 1),
                ("SunPy Project", path_to("about/project"), 1),
                ("Presentations", path_to("about/presentations"), 1),
                ("Community Roles", path_to("about/roles"), 1),
                ("Meetings", path_to("about/meetings"), 1),
                ("Code of Conduct", path_to("coc"), 1),
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
        ("Affiliated Packages", path_to("affiliated"), 1),
        ("Get Help", path_to("help"), 1),
        ("Contribute", path_to("contribute"), 1),
        ("Blog", path_to("blog"), 1),
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

    if not theme_options.get("sst_site_root"):
        theme_options["sst_site_root"] = "https://sunpy.org"

    if not theme_options.get("sst_is_root"):
        theme_options["sst_is_root"] = False

    if not theme_options.get("navbar_links"):
        theme_options["navbar_links"] = default_navbar
    # Let users pass a callable which take the sst_site_root to calculate the links
    elif iscallable(theme_options.get("navbar_links")):
        theme_options["navbar_links"] = theme_options["navbar_links"]
    else:
        theme_options["navbar_links"] = lambda path_to: theme_options["navbar_links"]

    if not theme_options.get("footer_links"):
        theme_options["footer_links"] = [
            ("Code", "https://github.com/sunpy", 1),
            ("Forum", "https://community.openastronomy.org/c/sunpy", 1),
            ("Chat", "https://openastronomy.element.io/#/room/#sunpy:openastronomy.org", 1),
        ]

    # TODO: This is nasty
    # Set the default value of show_source to False unless it's specified in the user config
    if "html_show_sourcelink" not in app.config._raw_config:
        app.config.html_show_sourcelink = False

    # Set the logo to the sunpy logo unless it's overriden in the user conifg
    if "html_logo" not in app.config._raw_config:
        app.config.html_logo = str(get_html_theme_path() / "static" / "img" / "sunpy_icon.svg")


def update_html_context(app: Sphinx, pagename: str, templatename: str, context, doctree) -> None:
    """
    Set extra things to use in jinja templates.
    """
    context["favicon_url"] = context.get("favicon_url", None) or "_static/img/sunpy_icon.svg"

    path_to = partial(lambda root, page: urljoin(root, page + ".html"), context["theme_sst_site_root"])
    if context["theme_sst_is_root"]:
        path_to = context["pathto"]
    context["theme_navbar_links"] = context["theme_navbar_links"](path_to)


# See https://github.com/pydata/pydata-sphinx-theme/blob/f6e1943c5f9fab4442f7e7d6f5ce5474833b66f6/src/pydata_sphinx_theme/__init__.py#L178
# Copied here to make footer_center behave like footer start and end
def update_and_remove_templates(app: Sphinx, pagename: str, templatename: str, context, doctree) -> None:
    """
    Update template names and assets for page build.
    """
    # Allow for more flexibility in template names
    template_sections = [
        "theme_footer_center",
    ]
    for section in template_sections:
        if context.get(section):
            # Break apart `,` separated strings so we can use , in the defaults
            if isinstance(context.get(section), str):
                context[section] = [ii.strip() for ii in context.get(section).split(",")]

            # Add `.html` to templates with no suffix
            for ii, template in enumerate(context.get(section)):
                if not os.path.splitext(template)[1]:
                    context[section][ii] = template + ".html"


def setup(app: Sphinx):
    # Register theme
    theme_dir = get_html_theme_path()
    app.add_html_theme("sunpy", theme_dir)
    app.add_css_file("sunpy_style.css")

    app.connect("builder-inited", update_config)
    app.connect("html-page-context", update_html_context)
    app.connect("html-page-context", update_and_remove_templates)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


_sunpy_static_path = get_html_theme_path() / "static"
ON_RTD = os.environ.get("READTHEDOCS", False) == "True"
SVG_ICON = _sunpy_static_path / "img" / "sunpy_icon.svg"
PNG_ICON = _sunpy_static_path / "img" / "sunpy_icon_128x128.png"

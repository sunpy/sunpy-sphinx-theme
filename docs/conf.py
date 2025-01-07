"""
Configuration file for the Sphinx documentation builder.
"""

import datetime
import os
import sys
from pathlib import Path

from sphinx_gallery.sorting import ExplicitOrder

from sunpy_sphinx_theme import SVG_ICON, _sunpy_static_path

# Add the test package to the path so we can import it for automodapi
sys.path.append(Path().absolute().as_posix())
# This serves as a check
import test_package  # NOQA: F401

project = "sunpy-sphinx-theme test docs"
author = "The SunPy Community"
copyright = f"{datetime.datetime.now(datetime.UTC).year}, {author}"  # NOQA: A001
extensions = [
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "hoverxref.extension",
    "matplotlib.sphinxext.plot_directive",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "sphinx_togglebutton",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sunpy_sphinx_theme.cards",
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = ".rst"
master_doc = "index"
default_role = "obj"
napoleon_use_rtype = False
intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3/",
        (None, "http://www.astropy.org/astropy-data/intersphinx/python3.inv"),
    ),
    "numpy": (
        "https://numpy.org/doc/stable/",
        (None, "http://www.astropy.org/astropy-data/intersphinx/numpy.inv"),
    ),
    "scipy": (
        "https://docs.scipy.org/doc/scipy/reference/",
        (None, "http://www.astropy.org/astropy-data/intersphinx/scipy.inv"),
    ),
    "matplotlib": (
        "https://matplotlib.org/",
        (None, "http://www.astropy.org/astropy-data/intersphinx/matplotlib.inv"),
    ),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/latest/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "skimage": ("https://scikit-image.org/docs/stable/", None),
    "drms": ("https://docs.sunpy.org/projects/drms/en/stable/", None),
    "parfive": ("https://parfive.readthedocs.io/en/latest/", None),
    "reproject": ("https://reproject.readthedocs.io/en/stable/", None),
}
html_theme = "sunpy"
html_static_path = [str(_sunpy_static_path), "_static"]
html_extra_path = ["_static/img"]
html_theme_options = {
    "footer_links": [
        ("Google", "https://google.com", 3),
        ("DDG", "https://duckduckgo.com", 3),
    ],
    "external_links": [
        {"name": "Python", "url": "https://www.python.org/"},
    ],
    "goatcounter_non_domain_endpoint": "https://sunpy-testing.goatcounter.com/count",
}
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Nfontsize=10",
    "-Nfontname=Helvetica Neue, Helvetica, Arial, sans-serif",
    "-Efontsize=10",
    "-Efontname=Helvetica Neue, Helvetica, Arial, sans-serif",
    "-Gfontsize=10",
    "-Gfontname=Helvetica Neue, Helvetica, Arial, sans-serif",
]
sphinx_gallery_conf = {
    "filename_pattern": "^((?!skip_).)*$",
    "examples_dirs": str(Path("..") / Path("examples")),
    "subsection_order": ExplicitOrder(
        [
            "../examples/section",
        ]
    ),
    "within_subsection_order": "ExampleTitleSortKey",
    "gallery_dirs": str(Path("generated") / Path("gallery")),
    "default_thumb_file": SVG_ICON,
    "abort_on_example_error": False,
    "plot_gallery": "True",
    "remove_config_comments": True,
}
if os.environ.get("READTHEDOCS"):
    hoverxref_api_host = "https://readthedocs.org"

    if os.environ.get("PROXIED_API_ENDPOINT"):
        # Use the proxied API endpoint
        # A RTD thing to avoid a CSRF block when docs are using a custom domain
        hoverxref_api_host = "/_"

hoverxref_auto_ref = False
hoverxref_domains = ["py"]
hoverxref_mathjax = True
hoverxref_modal_hover_delay = 500
hoverxref_tooltip_maxwidth = 600  # RTD main window is 696px
hoverxref_intersphinx = list(intersphinx_mapping.keys())
hoverxref_role_types = {
    # Roles within the py domain
    "attr": "tooltip",
    "class": "tooltip",
    "const": "tooltip",
    "data": "tooltip",
    "exc": "tooltip",
    "func": "tooltip",
    "meth": "tooltip",
    "mod": "tooltip",
    "obj": "tooltip",
    # Roles within the std domain
    "confval": "tooltip",
    "hoverxref": "tooltip",
    "ref": "tooltip",  # Would be used by hoverxref_auto_ref if we set it to True
    "term": "tooltip",
}
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

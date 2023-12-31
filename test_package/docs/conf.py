"""
Configuration file for the Sphinx documentation builder.
"""

import os
import datetime

from sphinx_gallery.sorting import ExampleTitleSortKey, ExplicitOrder

from sunpy_sphinx_theme import SVG_ICON

project = "Test Package"
author = "The Test Package Community"
copyright = f"{datetime.datetime.now().year}, {author}"
extensions = [
    "matplotlib.sphinxext.plot_directive",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "sphinx_gallery.gen_gallery",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
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
# Test out all the options for navbar_links
html_theme_options = {
    "navbar_links": [
        ("Home", "index.html", 1),
        ("Code Ref", "code_ref/index", 0),
        ("sunpy.org", "https://sunpy.org", 3),
        (
            "Dropdown",
            [
                ("SunPy Docs", "https://docs.sunpy.org", 3),
                ("About SunPy", "about/index.html", 2),
            ],
        ),
    ]
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
    "backreferences_dir": os.path.join("generated", "modules"),
    "filename_pattern": "^((?!skip_).)*$",
    "examples_dirs": os.path.join("..", "examples"),
    "subsection_order": ExplicitOrder(
        [
            "../examples/section",
        ]
    ),
    "within_subsection_order": ExampleTitleSortKey,
    "gallery_dirs": os.path.join("generated", "gallery"),
    "default_thumb_file": SVG_ICON,
    "abort_on_example_error": False,
    "plot_gallery": "True",
    "remove_config_comments": True,
    "doc_module": ("sunpy"),
}

"""Test conf file for a theme derived from the sunpy theme."""

from pathlib import Path

project = "SunPy Derived Theme Tests"
copyright = "2026, The SunPy Community"  # NOQA: A001
author = "The SunPy Community"

extensions = ["sunpy_sphinx_theme"]
html_theme = "derived"
html_static_path = []


def setup(app):
    """Register the derived theme with Sphinx."""
    app.add_html_theme("derived", str(Path(__file__).parent / "theme"))

"""
SunPy Sphinx Theme
==================

Based on the sphinx-bootstrap-theme.
"""
from pathlib import Path


def get_html_theme_path():
    """
    Return list of HTML theme paths.
    """
    theme_path = Path(__file__).parent.resolve() / "sunpy"
    return theme_path


def setup(app):
    """
    Setup.
    """
    theme_path = get_html_theme_path()
    app.add_html_theme("sunpy", str(theme_path))
    app.config.templates_path.append(str(theme_path / "templates"))

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

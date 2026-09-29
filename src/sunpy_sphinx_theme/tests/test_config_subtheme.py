"""
Tests relating to subthemes (i.e. astropy) setting config defaults.
"""
import logging
import re

from sunpy_sphinx_theme.tests.helpers import inline_scripts


def test_theme_defaults_of_derived_theme(sphinx_build_factory):
    """
    Test the theme.toml defaults of a theme derived from the sunpy theme.

    Given a minimal theme that derives from the sunpy theme and sets defaults in its theme.toml
    When the docs are built without any user theme options
    Then the derived defaults apply to the navbar, the footer, the site root links and the search config
    """
    sphinx_build = sphinx_build_factory("derived").build()
    html = sphinx_build.html_tree("index.html")

    # The derived navbar_links default renders in the navbar
    navbar = html.select_one("ul.bd-navbar-elements")
    home = navbar.select_one('a[href="https://example.org/index.html"]')
    assert home is not None
    assert home.text.strip() == "Home"
    docs = navbar.select_one('a[href="https://docs.example.org/"]')
    assert docs is not None
    assert docs.text.strip() == "Docs"

    # The derived footer_links default renders in the footer
    footer = html.select_one('.footer-links a[href="https://footer.example.org/"]')
    assert footer is not None
    assert footer.text.strip() == "Footer Example"

    # The derived rtd_search_projects default is used by the search config script
    search_config = [script for script in inline_scripts(html) if "set_search_config" in script]
    assert len(search_config) == 1
    assert '"name": "example"' in search_config[0]
    assert '"link": "https://example.org/docs/"' in search_config[0]

    # The sunpy theme.toml defaults still apply where the derived theme does not override
    assert '"label": "Load more results"' in search_config[0]


def test_no_search_projects(sphinx_build_factory, caplog):
    """
    Given a theme config where no sites are under "Documentation"
    When built
    Then RTD search config is disabled
    """
    config_toml = """\
    [theme]
    inherit = "sunpy"

    [options]
    sst_site_root = "https://astropy.org"

    navbar_links = [
        ["Home", "index.html", 2],
        ["astropy", "https://docs.astropy.org/", 3],
    ]
    """
    sphinx_build = sphinx_build_factory("derived", files={"theme/theme.toml": config_toml}).build()
    html = sphinx_build.html_tree("index.html")
    search_config = [script for script in inline_scripts(html) if "set_search_config" in script]
    assert len(search_config) == 0

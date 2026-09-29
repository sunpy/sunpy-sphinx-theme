"""Tests for the goat counter analytics assets registered by the theme."""

import pytest

from sunpy_sphinx_theme.tests.helpers import inline_scripts, script_srcs

SUNPY_GOAT_URL = "https://sunpy.goatcounter.com/count"
GOATCOUNTER_COUNT_JS = "https://gc.zgo.at/count.js"


def goatcounter_inline_script(html_tree):
    """Return the inline script that configures window.goatcounter."""
    scripts = [script for script in inline_scripts(html_tree) if "window.goatcounter" in script]
    assert len(scripts) == 1
    return scripts[0]


def test_goatcounter_default_sunpy_site(sphinx_build_factory):
    """
    Test the goat counter default for the sunpy site root.

    Given the docs are built with the default theme options
    When a page is rendered
    Then the inline script configures the sunpy goat counter and the goat counter script is loaded async
    """
    sphinx_build = sphinx_build_factory("base").build()
    html = sphinx_build.html_tree("index.html")

    # The inline script configures window.goatcounter for the sunpy domain
    script = goatcounter_inline_script(html)
    assert "var endpoint = '';" in script
    assert "location.hostname.endsWith('sunpy.org')" in script
    assert f"endpoint = '{SUNPY_GOAT_URL}'" in script

    # The goat counter script itself is loaded async
    count_js = html.select(f'script[src="{GOATCOUNTER_COUNT_JS}"]')
    assert len(count_js) == 1
    assert count_js[0].attrs["async"] == "async"


def test_goatcounter_disabled_for_non_sunpy_site(sphinx_build_factory):
    """
    Test the goat counter for a non-sunpy site root.

    Given the site root is a non-sunpy domain with no explicit goat counter URL
    When a page is rendered
    Then no goat counter assets are registered
    """
    confoverrides = {"html_theme_options": {"sst_site_root": "https://docs.example.org"}}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    html = sphinx_build.html_tree("index.html")

    assert not [script for script in inline_scripts(html) if "window.goatcounter" in script]
    assert GOATCOUNTER_COUNT_JS not in script_srcs(html)


@pytest.mark.parametrize("scheme", ["https", "http"])
def test_goatcounter_custom_url_for_non_sunpy_site(sphinx_build_factory, scheme):
    """
    Test an explicit goat counter URL for a non-sunpy site root.

    Given the site root is a non-sunpy domain with an explicit goat counter URL
    When a page is rendered
    Then the inline script checks the site root without its scheme and uses the explicit URL
    """
    confoverrides = {
        "html_theme_options": {
            "sst_site_root": f"{scheme}://docs.example.org",
            "goatcounter_analytics_url": "https://example.goatcounter.com/count",
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    html = sphinx_build.html_tree("index.html")

    script = goatcounter_inline_script(html)
    assert "location.hostname.endsWith('docs.example.org')" in script
    assert "endpoint = 'https://example.goatcounter.com/count'" in script
    assert GOATCOUNTER_COUNT_JS in script_srcs(html)


@pytest.mark.parametrize("disabled_value", [None, ""])
def test_goatcounter_explicitly_disabled(sphinx_build_factory, disabled_value):
    """Test explicitly disabling the goat counter.

    Given the goat counter URL is set to a falsy value
    When a page is rendered
    Then no goat counter assets are registered
    """
    confoverrides = {"html_theme_options": {"goatcounter_analytics_url": disabled_value}}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    html = sphinx_build.html_tree("index.html")

    assert not [script for script in inline_scripts(html) if "window.goatcounter" in script]
    assert GOATCOUNTER_COUNT_JS not in script_srcs(html)


@pytest.mark.parametrize(
    ("endpoint", "default_line"),
    [
        ("https://test.example.com/count", "var endpoint = 'https://test.example.com/count';"),
        (False, "var endpoint = '';"),
    ],
)
def test_goatcounter_non_domain_endpoint(sphinx_build_factory, endpoint, default_line):
    """Test the non-domain endpoint of the goat counter.

    Given goatcounter_non_domain_endpoint is set to a URL or False
    When a page is rendered
    Then the default endpoint in the inline script matches the configured value
    """
    confoverrides = {"html_theme_options": {"goatcounter_non_domain_endpoint": endpoint}}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    html = sphinx_build.html_tree("index.html")

    script = goatcounter_inline_script(html)
    assert default_line in script


def test_goatcounter_astropy(sphinx_build_factory):
    """
    Test astropy configuration setup.

    Given the site root is astropy.org and the goat counter url is set.
    When a page is rendered
    Then the inline script adds the astropy goatcounter only on astropy.org sites.
    """
    confoverrides = {
        "html_theme_options": {
            "sst_site_root": "https://astropy.org",
            "goatcounter_analytics_url": "https://astropy.goatcounter.com/count",
        },
    }
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    html = sphinx_build.html_tree("index.html")

    script = goatcounter_inline_script(html)
    assert "var endpoint = '';" in script
    assert "location.hostname.endsWith('astropy.org')" in script
    assert "endpoint = 'https://astropy.goatcounter.com/count'" in script
    assert GOATCOUNTER_COUNT_JS in script_srcs(html)

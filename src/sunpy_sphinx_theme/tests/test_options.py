from sunpy_sphinx_theme.tests.helpers import script_srcs, stylesheet_hrefs


def test_rtd_search_disabled(sphinx_build_factory):
    """Test disabling the search assets.

    Given rtd_search is disabled
    When a page is rendered
    Then the search assets are not registered and the goat counter and submenu assets are unaffected
    """
    confoverrides = {"html_theme_options": {"rtd_search": False}}
    sphinx_build = sphinx_build_factory("base", confoverrides=confoverrides).build()
    html = sphinx_build.html_tree("index.html")

    srcs = script_srcs(html)
    assert not any("js/rtd_enhanced_search.js" in src for src in srcs)
    assert not any("css/rtd_enhanced_search.css" in href for href in stylesheet_hrefs(html))

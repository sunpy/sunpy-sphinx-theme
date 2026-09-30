"""
Using Axe-core, scan the documentation pages for accessibility violations.
Note that in contrast with the rest of our tests, the accessibility tests in this file
are run against a build of our test documentation, not purposely-built test sites.
"""

from urllib.parse import urljoin

import pytest

# Using importorskip to ensure these tests are only loaded if Playwright is installed.
playwright = pytest.importorskip("playwright")
from playwright.sync_api import Page, expect  # noqa: E402

# Important note: automated accessibility scans can only find a fraction of
# potential accessibility issues.
#
# This test file scans pages from our documentation with a JavaScript library
# called Axe-core, which checks the page for accessibility violations, such as
# places on the page with poor color contrast that would be hard for people
# with low vision to see.
#
# Just because a page passes the scan with no accessibility violations does
# *not* mean that it will be generally usable by a broad range of disabled
# people. It just means that page is free of common testable accessibility
# pitfalls.


def filter_ignored_violations(violations, url_pathname, theme):
    """Filter out ignored axe-core violations.

    In some tests, we wish to ignore certain accessibility violations that we
    won't ever fix or that we don't plan to fix soon.
    """
    new_violations = []

    for violation in violations:
        ignore = False

        # TODO: Our light theme link color does not pass, either fix it or just accept it
        if violation["id"] == "color-contrast" and theme == "light":
            ignore = True
        # This one is probably fine, it's the headings inside the popup
        if url_pathname == "/cards.html" and violation["id"] == "heading-order":
            ignore = True

        if url_pathname == "/subsections.html" and violation["id"] in ("region", "summary-name"):
            ignore = True

        if url_pathname == "/index.html" and violation["id"] in ("region", "summary-name"):
            ignore = True

        if not ignore:
            new_violations.append(violation)

    # No violations are currently ignored for our documentation pages. When a
    # violation is found that we do not plan to fix, filter it out here by
    # url_pathname and rule id, in the same manner as the pydata-sphinx-theme
    # does in its tests/test_a11y.py.
    return new_violations


def format_violations(violations):
    """Return a pretty string representation of Axe-core violations."""
    result = f"""

        Found {len(violations)} accessibility violation(s):
        """

    for violation in violations:
        result += f"""

            - Rule violated:
              {violation["id"]} - {violation["help"]}
                - URL: {violation["helpUrl"]}
                - Impact: {violation["impact"]}
                - Tags: {" ".join(violation["tags"])}
                - Targets:"""

        for node in violation["nodes"]:
            for target in node["target"]:
                result += f"""
                    - {target}"""

        result += "\n\n"

    return result


@pytest.mark.a11y
@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize(
    ("url_pathname", "selector"),
    [
        # The Kitchen Sink page of our test documentation
        ("/colors.html", "#colors"),
        ("/colors.html", "#admonitions"),
        ("/colors.html", "#snippets"),
        # The theme configuration page, including the header and footer
        # elements it renders (navbar links, footer links, footer center)
        ("/customizing.html", "#customizing-the-theme"),
        ("/customizing.html", "#changing-the-theme-settings"),
        ("/customizing.html", "#adjusting-the-styling"),
        # The sphinx-design components used by our documentation
        ("/web-components.html", "#sphinx-design-components"),
        ("/web-components.html", "#badges-and-button-links"),
        ("/web-components.html", "#cards"),
        ("/web-components.html", "#tabs"),
        ("/web-components.html", "#dropdowns"),
        ("/web-components.html", "#copybuttons"),
        ("/web-components.html", "#toggle-buttons"),
        # The cards and tables provided by the theme cards extension
        ("/cards.html", "#cards-and-tables"),
        # Pages with deeply nested toctrees to stress the sidebar navigation
        ("/subsections.html", ""),
        # Using one of the simplest pages on the site, select the whole page
        # for testing in order to effectively test repeated website elements
        # like nav, sidebars, breadcrumbs, footer
        ("/index.html", ""),  # select whole page
    ],
)
def test_axe_core(
    page: Page,
    url_base: str,
    theme: str,
    url_pathname: str,
    selector: str,
):
    """Should have no Axe-core violations at the provided theme and page section."""
    # Load the page at the provided path
    url_full = urljoin(url_base, url_pathname)
    page.goto(url_full)

    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")

    # Wait for CSS transitions (Bootstrap's transitions are 300 ms)
    page.wait_for_timeout(301)

    # Inject the Axe-core JavaScript library into the page
    page.add_script_tag(path="node_modules/axe-core/axe.min.js")

    # Run the Axe-core library against a section of the page (unless the
    # selector is empty, then run against the whole page)
    results = page.evaluate("axe.run()" if selector == "" else f"axe.run('{selector}')")

    # Check found violations against known violations that we do not plan to fix
    filtered_violations = filter_ignored_violations(results["violations"], url_pathname, theme)

    assert len(filtered_violations) == 0, format_violations(filtered_violations)


@pytest.mark.a11y
def test_code_block_tab_stop(page: Page, url_base: str) -> None:
    """Code blocks that have scrollable content should be tab stops."""
    page.set_viewport_size({"width": 1440, "height": 720})
    page.goto(urljoin(url_base, "/customizing.html"))

    # This code-block contains a line long enough to overflow at narrow
    # viewport widths (the "rtd_search_projects" example with a URL in it)
    code_block = page.locator("css=#rtd-search-projects pre", has_text="rtd_search_projects")

    # Viewport is wide, so code block content fits, no overflow, no tab stop
    assert code_block.evaluate("el => el.scrollWidth > el.clientWidth") is False
    assert code_block.evaluate("el => el.tabIndex") != 0

    page.set_viewport_size({"width": 400, "height": 720})

    # Narrow viewport, content overflows ...
    assert code_block.evaluate("el => el.scrollWidth > el.clientWidth") is True

    # ... and code block should be a tab stop.
    #
    # Note: expect() will wait until the expect condition is true (up to the
    # test timeout limit). This is important because the resize handler is
    # debounced.
    expect(code_block).to_have_attribute("tabindex", "0")

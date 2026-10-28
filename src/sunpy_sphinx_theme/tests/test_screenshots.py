from urllib.parse import urljoin

import pytest


@pytest.mark.mpl_image_compare
@pytest.mark.parametrize(
    "viewport",
    [
        pytest.param((820, 600), id="tablet width"),
        pytest.param((1920, 1080), id="larger-pc"),
    ],
)
@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize(
    "url_pathname",
    [
        "/colors.html",
        "/customizing.html",
        "/web-components.html",
        "/cards.html",
        "/subsections.html",
        "/index.html",
    ],
)
def test_screenshots_sst_docs(
    url_base,
    url_pathname,
    theme,
    viewport,
    screenshot,
    page,
):
    url_full = urljoin(url_base, url_pathname)
    page.goto(url_full)

    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
    # Run a line of JavaScript that sets the light/dark theme on the page
    page.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
    return screenshot.from_locator(page)

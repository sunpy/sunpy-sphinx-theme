def inline_scripts(html_tree):
    """Return the content of all inline scripts in a page."""
    return [script.string for script in html_tree.select("script") if script.string]


def script_srcs(html_tree):
    """Return the src URLs of all external scripts in a page."""
    return [script["src"] for script in html_tree.select("script[src]")]


def stylesheet_hrefs(html_tree):
    """Return the hrefs of all stylesheets in a page."""
    return [link["href"] for link in html_tree.select("link[rel='stylesheet']")]

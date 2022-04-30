# SunPy Sphinx Theme

[![PyPI version](https://badge.fury.io/py/sunpy-sphinx-theme.svg)](https://badge.fury.io/py/sunpy-sphinx-theme)

This repository contains the sphinx theme used by the Sunpy Project for its website and documentation.

To use put this in your `conf.py` file:

    from sunpy_sphinx_theme.conf import *

and make sure you do not have the `html_theme` variable defined elsewhere in `conf.py`.

## Dropdown

If you want to add entries to the dropdown menus you can find them in `sunpy_sphinx_theme/conf.py`.

If you want to override a link in your build of a project.
You should be able to replace the entries in your project's `conf.py`.

This should override the URL for the code of conduct.

```python
html_theme_option["navbar_links"][0][-1][1] = NEW_URL
```

## Sidebar

We do not have a recursive check for the sidebar on all pages.

If you want to add pages to the sidebar you can find ``html_sidebars`` in `sunpy_sphinx_theme/conf.py`.

You will want to add to this in your own packages ``conf.py``

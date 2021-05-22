# SunPy Sphinx Theme

[![PyPI version](https://badge.fury.io/py/sunpy-sphinx-theme.svg)](https://badge.fury.io/py/sunpy-sphinx-theme)

This repository contains the still work in progress sphinx theme for the new website and documentation.

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

## Metadata

If you want to use the OpenGraph settings correctly you will need to add the following variables in `conf.py`:

*. base_url : This is the base url of where the docs or website will be hosted.
*. opengraph_imageurl: This is the url of where the image will be stored in the final built version.
*. seo_description: Description of the project build.

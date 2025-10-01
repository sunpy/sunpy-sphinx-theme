.. _customizing:

Customizing the Theme
=====================

While all the default settings and styling for this theme are for the sunpy.org site, we have endeavored to make all the settings configurable.

Changing the Theme Settings
---------------------------

As well as all the default configuration settings we inherit from the pydata-sphinx-theme the sunpy-sphinx-theme provides the following configuration options.
All of these options should be set inside the ``html_theme_options`` dictionary in your ``conf.py`` file.

General Configuration
^^^^^^^^^^^^^^^^^^^^^

``footer_center``
#################

This is the path to a template or a list of templates to render in the middle segment of the footer.
It behaves the same as ``footer_start`` or ``footer_end`` from pydata-sphinx-theme.

``sst_site_root``
#################

This is the root URL for all the relative links in the top navbar when ``sst_is_root`` is `False`.
This functionality allows you to have a sphinx project where instead of linking to the absolute URL of some or all of the links in the topnav bar they are relative to that sphinx build instead.

``sst_is_root``
###############

Set this to true if you are building the project which will be deployed to ``sst_site_root``.

If this is set to `True` then this sphinx build is the root of your many-sphinx trees and links in the topnav (see below) should be relative to this site and not the ``sst_site_root`` configuration variable.

``navbar_links``
################

This is a list of tuples specifying the links to place in the top navbar.
An element of this list takes the form ``(title, document, relative_to)``.
``title`` is the text to be rendered for the link.
``document`` is a reference to a document or an absolute URL.
``relative_to`` controls how the ``document`` parameter is interpreted.

The links in ``navbar_links`` are parsed using a wrapper around sphinx's builtin `pathto <https://www.sphinx-doc.org/en/master/development/templating.html#pathto>`__ function.
If you want to reference things relative to the current sphinx build for every project built with the theme (i.e., they all have an about page at the site root) then you can pass ``0`` or ``1`` here to mimic the behavior of the sphinx builtin.
If you want to pass an absolute URL through set ``relative_to`` to ``3``.
If you want to pass a document which is relative to ``sst_site_root`` when ``sst_is_root`` is False and relative to the current sphinx build when it's True then set ``relative_to`` to ``2``.

It's possible to add dropdown menus to the topnav by setting document equal to a list of tuples following the same format.

``footer_links``
################

Footer links are a number of links which will get placed in the center of the footer.
They are specified in the same format as the ``navbar_links``.

Analytics with Goat Counter
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The theme supports using `Goat Counter <https://www.goatcounter.com/>`__ to monitor traffic. Goat Counter is an Open Source project with free hosting, so a good fit for many projects using this theme.
GoatCounter support is enabled by default for the ``sunpy.org`` domain, so if your ``sst_site_root="https://sunpy.org"`` then it will be enabled with the default SunPy settings.
To enable it for other sites you need to do configure the following options.

``goatcounter_analytics_url``
#############################

This is the analytics URL for the GoatCounter project, for example ``"https://sunpy.goatcounter.com/count"``.

``goatcounter_non_domain_endpoint``
###################################

This setting configures how analytics work for domains which are not ``sst_site_root`` or subdomains of the root.
The default is ``False`` meaning that if the domain isn't ``sst_site_root`` then GoatCounter is disabled.
If you set this to a GoatCounter endpoint (such as ``goatcounter_analytics_endpoint`` then that endpoint will be used for domains which are not ``sst_site_root``.


Read the Docs Search
^^^^^^^^^^^^^^^^^^^^

The theme supports an enhanced version of the `Server Side Search <https://docs.readthedocs.com/platform/stable/server-side-search/index.html>`__ Read the Docs add-on.
This adds a similar UI, but enables searching multiple Read the Docs projects simultaneously, not just the current RTD project and all subprojects as supported by the official add-on.
This means that when configured this enables all RTD projects using the theme to search all others, i.e. if you have a parent project "sunpy" and a subproject "ndcube" this search allows users in the "ndcube" documentation to also search "sunpy", whereas the official one only allows users in "sunpy" to also search "ndcube".

This is enabled by default, but will not work unless accessing the documentation via Read the Docs, if the enhanced search fails for any reason it will fallback to the standard sphinx search.
To facilitate debugging of this extension, it supports proxying requests to the RTD search API through the `corsproxy.io <https://corsproxy.io>`__ service if the ``?debug`` query parameter is set on the URL, set this if testing the search on a local build.

``rtd_search``
##############

Enable or disable the RTD search functionality. Defaults to ``True``.

``rtd_search_projects``
#######################

This configuration option is the list of projects that the search will query the RTD API for results.
By default this configuration uses all the links in ``navbar_links``.
The format of this option is a list of dictionaries with ``"name"`` and ``"links"`` keys, i.e.:

.. code-block:: python

   rtd_search_projects = [
       {"name": "sunpy", "link": "https://docs.sunpy.org"}
   ]


``rtd_search_load_more_label``
##############################

This is the label shown on the button to load more results from the RTD API.
The default is ``"Load more results"``.

``rtd_search_no_results_label``
###############################

This is the label shown when no results match the query.
The default is ``"There are no results for this search"``.

Adjusting the Styling
---------------------

This theme makes some minor CSS tweaks from the pydata-sphinx-theme both to adjust the styling for SunPy's branding and to make our customisations work.
We have tried to use CSS variables to control the styling the key variables are:

.. code-block:: css

  --sst-accent-color-bright
  --sst-accent-color-muted
  --sst-dark-color
  --sst-darker-color
  --sst-darkest-color
  --sst-lightest-color
  --sst-lighter-color
  --sst-light-color
  --sst-header-background: var(--sst-dark-color);
  --sst-header-text: var(--sst-lighter-color);
  --sst-sidebar-background-color: var(--pst-color-background);

The included CSS uses "light" (light, lighter, lightest) colors for the background on the light theme and "dark" colors for the text, and the inverse on the dark theme.
The bright accent color is used for some text (e.g. links) on the dark theme, and the muted variant on the light theme to increase contrast.

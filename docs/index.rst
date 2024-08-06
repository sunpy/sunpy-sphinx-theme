sunpy-sphinx-theme
==================

The ``sunpy-sphinx-theme`` is a `sphinx` theme designed for the needs of the SunPy Project's main website and subproject documentation pages.
It's primary goals are:

* To provide a consistent look and feel over all the sunpy.org websites and subdomains.
* To give all documentation pages maintained by the SunPy project a branded appearance.
* To provide a global navigation bar over all these sites so that it is possible to navigate between the sunpy.org site and all the documentation.

Version 2 of this package achieves this by being a sub-theme of the `pydata-sphinx-theme` with a heavily modified header bar.
The core changes between this theme and the `pydata-sphinx-theme` are:

* Remove the toctree navigation from the header bar and place it all in the sidebar (in the same manner as sphinx-book-theme).
* Add links to the header bar which are specified as theme config variables, with defaults for sunpy.org.
* Add a center element to the footer bar.
* Restyled the theme for SunPy colors.
* Added optional support for analytics though `goatcounter.com <https://www.goatcounter.com/>`__ which defaults to on for sunpy.org domains.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card::
      :class-card: card

      Documentation
      ^^^^^^^^^^^^^

      .. toctree::
            :maxdepth: 1

            customizing
            colors
            web-components
            cards

   .. grid-item-card::
      :class-card: card

      Examples
      ^^^^^^^^

      .. toctree::
            :maxdepth: 1

            generated/gallery/index
            code_ref/index

   .. grid-item-card::
      :class-card: card
      :link: subsections
      :link-type: ref

      Conventions
      ^^^^^^^^^^^

      .. toctree::
            :maxdepth: 1

            subsections
            subsections_toc

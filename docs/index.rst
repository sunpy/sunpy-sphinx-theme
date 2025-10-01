sunpy-sphinx-theme
==================

The ``sunpy-sphinx-theme`` is a `sphinx` theme designed for the needs of the SunPy Project's main website and subproject documentation pages.
It's primary goals are:

* To provide a consistent look and feel over all the separate documentation sites for the project.
* To give all documentation pages maintained a consistent branded appearance.
* To provide a global navigation bar over all these sites so that it is possible to navigate between the sunpy.org site and all the documentation.

Version 2 of this package achieves this by being a sub-theme of the `pydata-sphinx-theme` with a heavily modified header bar.
The core changes between this theme and the `pydata-sphinx-theme` are:

* Remove the toctree navigation from the header bar and place it all in the sidebar (in the same manner as sphinx-book-theme).
* Add links to the header bar which are specified as theme config variables, so they are the same over all sites.
* Add a center element to the footer bar.
* Restyled the theme for SunPy colors.
* Added optional support for analytics though `goatcounter.com <https://www.goatcounter.com/>`__ which defaults to on for sunpy.org domains.
* Added optional support for a multi-project Read the Docs search interface.

The theme is highly configurable, although the defaults are for the SunPy project, this theme can be used for other organisations where they have multiple documentation sites and want a unified user experience.
For information on how to configure this theme for your site see :ref:`customizing`.

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

.. COPY FROM PYDATA THEME DOCS

Color
*****

This theme specifies color variables for the primary and secondary colors (``--pst-color-primary`` and ``--pst-color-secondary``, respectively).
These are meant to complement one another visually across the theme, if you modify these, choose colors that look good when paired with one another.
There are also several other color variables that control the color for admonitions, links, menu items, etc.

Each color variable has two values, one corresponding to the "light" and one for the "dark" theme.
These are used throughout many of the theme elements to define text color, background color, etc.

Here is an overview of the colors available in the theme (change theme mode to switch from light to dark versions).

.. raw:: html

        <style>
        span.pst-primary {background-color: var(--pst-color-primary);}
        span.pst-secondary {background-color: var(--pst-color-secondary);}
        span.pst-accent {background-color: var(--pst-color-accent);}
        span.pst-success {background-color: var(--pst-color-success);}
        span.pst-info {background-color: var(--pst-color-info);}
        span.pst-warning {background-color: var(--pst-color-warning);}
        span.pst-danger {background-color: var(--pst-color-danger);}
        span.pst-background {background-color: var(--pst-color-background);}
        span.pst-on-background {background-color: var(--pst-color-on-background);}
        span.pst-surface {background-color: var(--pst-color-surface);}
        span.pst-on-surface {background-color: var(--pst-color-on-surface);}
        span.pst-target {background-color: var(--pst-color-target);}
        </style>

        <p>
        <span class="sd-sphinx-override sd-badge pst-badge pst-primary sd-bg-text-primary">primary</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-secondary sd-bg-text-secondary">secondary</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-accent sd-bg-text-secondary">accent</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-success sd-bg-text-success">success</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-info sd-bg-text-info">info</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-warning sd-bg-text-warning">warning</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-danger sd-bg-text-danger">danger</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-background">background</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-on-background">on-background</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-surface">surface</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-on-surface sd-bg-text-primary">on-surface</span>
        <span class="sd-sphinx-override sd-badge pst-badge pst-target">target</span>
        </p>


**To modify the colors for these variables** for light and dark themes, :ref:`add a custom CSS stylesheet <custom-css>` with a structure like so:

.. code-block:: css

    html[data-theme="light"] {
        --pst-color-primary: black;
    }

    html[data-theme="dark"] {
        --pst-color-primary: white;
    }

This theme uses shadows to convey depth in the light theme mode and opacity in the dark one.
It defines 4 color variables that help build overlays in your documentation.

- :code:`background`: color of the back-most surface of the documentation
- :code:`on-background` elements that are set on top of this background (e.g. the header navbar on dark mode).
- :code:`surface` elements set on the background with a light-grey color in the light theme mode. This color has been kept in the dark theme (e.g. code-block directives).
- :code:`on-surface` elements that are on top of :code:`surface` elements (e.g. sidebar directives).

The following image should help you understand these overlays:

.. raw:: html

    <style>
        /* use https://unminify.com to check the indented version of the overlay component */
        .overlay-container {margin-top: 10%; left: 20%; --width: 80%; --height: 200px; width: var(--width); height: var(--height); position: relative;}
        .overlay-container .pst-overlay {position: absolute; border: 2px solid var(--pst-color-border);}
        .overlay-container .pst-background {background-color: var(--pst-color-background); width: var(--width); transform: skew(-45deg); height: var(--height);}
        .overlay-container .pst-on-background {background-color: var(--pst-color-on-background); height: var(--height); width: calc(var(--width) / 3); transform: skew(-45deg) translate(-2rem, -2rem);}
        .overlay-container .pst-surface {background-color: var(--pst-color-surface); height: var(--height); width: calc(var(--width) / 3); transform: skew(-45deg) translate(-2rem, -2rem); left: calc(var(--width) / 3 * 2);}
        .overlay-container .pst-on-surface {background-color: var(--pst-color-on-surface); width: calc(var(--width) / 3); height: calc(var(--height) * 0.66); transform: skew(-45deg) translate(-2rem, -4rem); left: calc(var(--width) / 3 * 2);}
        .overlay-container .label {position: absolute; bottom: 0.5rem; left: 50%; transform: skew(45deg) translateX(-50%); white-space: nowrap;}
    </style>

    <div class="overlay-container">
    <div class="pst-overlay pst-background">
    <p class="label">background</p>
    </div>
    <div class="pst-overlay pst-on-background">
    <p class="label">on-background</p>
    </div>
    <div class="pst-overlay pst-surface">
    <p class="label">surface</p>
    </div>
    <div class="pst-overlay pst-on-surface">
    <p class="label sd-bg-text-primary">on-surface</p>
    </div>
</div>

Documentation
*************

Documentation :any:`index <genindex>` and :any:`Module <modindex>` index.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card::
        :class-card: card

        Getting started
        ^^^^^^^^^^^^^^^

        .. toctree::
            :maxdepth: 3

            generated/gallery/index
            code_ref/index

    .. grid-item-card::
        :class-card: card
        :link: subsections
        :link-type: ref

        Conventions
        ^^^^^^^^^^^

        .. toctree::
            :maxdepth: 3

            subsections
            subsections_toc

Some code:

.. code-block:: python

    """
    Parameters
    ----------
    x : `type`
       Description of parameter x.
    """

It's good to have your upstream remote have a scary name [#]_, to remind you that it's a read-write remote::

    $ git remote add upstream-rw git@github.com:sunpy/sunpy.git
    $ git fetch upstream-rw

.. [#] Text of the first footnote.

Colors
------

Copied from the pydata-sphinx theme docs, here's the colours used.
These colors change between the dark and light themes.

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
  span.pst-link {background-color: var(--pst-color-link);}
  span.pst-code {background-color: var(--pst-color-code);}
  span.pst-inline-code {background-color: var(--pst-color-inline-code);}
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
  <span class="sd-sphinx-override sd-badge pst-badge pst-link">link</span>
  <span class="sd-sphinx-override sd-badge pst-badge pst-code">code</span>
  <span class="sd-sphinx-override sd-badge pst-badge pst-inline-code">inline code</span>
  </p>

Testing
-------

``:func:``
:func:`numpy.mean`

``:meth:``
:meth:`numpy.mean`

``:class:``
:class:`numpy.mean`

Normal
`numpy.mean`

``:func:``
:func:`numpy.ndarray.mean`

``:meth:``
:meth:`numpy.ndarray.mean`

``:class:``
:class:`numpy.ndarray.mean`

Normal
`numpy.ndarray.mean`

Sometimes you need a URL: `bbc.com <https://www.bbc.co.com>`__

Contributing to ``sunraster``

Admonitions
-----------

.. admonition:: Generic Admonition

   You can make up your own admonition too.

.. attention:: attention
.. caution:: caution
.. danger:: danger
.. error:: error
.. hint:: hint
.. important:: important
.. note:: note
.. tip:: tip
.. warning:: warning

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

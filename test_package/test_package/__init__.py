"""
This module provies a collection of functions.
"""
from sunpy.util.decorators import deprecated

__all__ = [
    "Animal",
    "function",
    "a_really_long_function_name_just_to_see_what_happens",
]


@deprecated("1.0", alternative="sunpy.net.Fido")
class Animal:
    """
    A deprecated class used to represent an Animal.

    .. note::

        * This is a note.

    .. warning::

        * This is a warning.

    Attributes
    ----------
    name : `str`
        The name of the animal.
    sound : `str`
        The sound that the animal makes.
    num_legs : int
        The number of legs the animal has (default 4).

    Examples
    --------
    >>> import datetime
    >>> datetime.datetime(2019, 8, 16, 22, 46, 37, 856437)
    datetime.datetime(2019, 8, 16, 22, 46, 37, 856437)

    References
    ----------
    * https://realpython.com/documenting-python-code/
    """

    says_str = "A {name} says {sound}"

    def __init__(self, name, sound, num_legs=5):
        """
        Parameters
        ----------
        name : `str`
            The name of the animal.
        sound : `str`
            The sound the animal makes.
        num_legs : int, optional
            The number of legs the animal (default is 5).
        """

        self.name = name
        self.sound = sound
        self.num_legs = num_legs

    def says(self, sound=None):
        """
        Prints what the animals name is and what sound it makes.

        If the argument `sound` isn't passed in, the default animal
        sound is used.

        Parameters
        ----------
        sound : `str`, optional
            The sound the animal makes (default is `None`),

        Raises
        ------
        `NotImplementedError`
            If no sound is set for the animal or passed in as a
            parameter.

        References
        ----------
        * `A URL. <www.sunpy.org>`__
        """

        if self.sound is None and sound is None:
            raise NotImplementedError("Silent Animals are not supported!")

        out_sound = self.sound if sound is None else sound
        print(self.says_str.format(name=self.name, sound=out_sound))


def function():
    """
    Prints what the animals name is and what sound it makes.

    If the argument `sound` isn't passed in, the default animal
    sound is used.

    .. note::

        * This is a note.

    .. warning::

        * This is a warning.

    Parameters
    ----------
    sound : `str`, optional
        The sound the animal makes (default is `None`).

    Returns
    -------
    `list`
        A list.

    Raises
    ------
    `NotImplementedError`
        If no sound is set for the animal or passed in as a
        parameter.

    Examples
    --------
    >>> import datetime
    >>> datetime.datetime(2019, 8, 16, 22, 46, 37, 856437)
    datetime.datetime(2019, 8, 16, 22, 46, 37, 856437)

    References
    ----------
    * `A URL. <www.sunpy.org>`__
    """

    print("A SOUND")


def a_really_long_function_name_just_to_see_what_happens():
    """
    Prints what the animals name is and what sound it makes.

    If the argument `sound` isn't passed in, the default animal
    sound is used.

    .. note::

        * This is a note.

    .. warning::

        * This is a warning.

    Parameters
    ----------
    sound : `str`, optional
        The sound the animal makes (default is `None`).

    Returns
    -------
    `list`
        A list.

    Raises
    ------
    `NotImplementedError`
        If no sound is set for the animal or passed in as a
        parameter.

    Examples
    --------
    >>> import datetime
    >>> datetime.datetime(2019, 8, 16, 22, 46, 37, 856437)
    datetime.datetime(2019, 8, 16, 22, 46, 37, 856437)

    References
    ----------
    * `A URL. <www.sunpy.org>`__
    """

    print("A SOUND")

from setuptools import setup, find_packages

from sunpy_sphinx_theme import __version__

setup(
    name="sunpy-sphinx-theme",
    version=__version__,
    use_2to3=False,
    description="The sphinx theme for the SunPy website and documentation.",
    long_description="",
    author="The SunPy Developers",
    install_requires=[
        "setuptools",
        "sphinx",
        "sphinx-bootstrap-theme"
    ],
    packages=['sunpy_sphinx_theme'],
    include_package_data=True,
)

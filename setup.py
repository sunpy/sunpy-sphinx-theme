from setuptools import setup, find_packages

setup(
    name="sunpy-sphinx-theme",
    version="1.0.6",
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

# -- Project information -----------------------------------------------------
from datetime import datetime

project = "sunpy-sphinx-theme"
copyright = f"{datetime.now().year}, The SunPy Project"
author = "The SunPy Project"
release = "2.0"

# -- General configuration ---------------------------------------------------
extensions = []
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sunpy"

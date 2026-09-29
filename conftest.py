"""Configuration of the pytest session."""

from __future__ import annotations

import sys
import time
from http.client import HTTPConnection
from os import environ
from pathlib import Path
from shutil import copytree
from subprocess import PIPE, Popen
from typing import TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from collections.abc import Callable

    from sphinx.testing.util import SphinxTestApp

pytest_plugins = "sphinx.testing.fixtures"

repo_path = Path(__file__).parent
tests_path = repo_path / "src" / "sunpy_sphinx_theme" / "tests"
docs_build_path = repo_path / "docs" / "_build" / "html"


# -- global fixture to build sphinx tmp docs ---------------------------------


class SphinxBuild:
    """Helper class to build a test documentation."""

    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src

    def build(self, *, no_warning: bool = True) -> SphinxBuild:
        """Build the application."""
        self.app.build()
        if no_warning is True:
            assert self.warnings == "", self.status
        return self

    @property
    def status(self) -> str:
        """Returns the status of the current build."""
        return self.app.status.getvalue()

    @property
    def warnings(self) -> str:
        """Returns the warnings raised by the current build."""
        return self.app.warning.getvalue()

    @property
    def outdir(self) -> Path:
        """Returns the output directory of the current build."""
        return Path(self.app.outdir)

    def html_tree(self, *path) -> BeautifulSoup:
        """Returns the html tree of the current build."""
        path_page = self.outdir.joinpath(*path)
        if not path_page.exists():
            msg = f"{path_page} does not exist"
            raise ValueError(msg)
        return BeautifulSoup(path_page.read_text("utf8"), "html.parser")


@pytest.fixture
def sphinx_build_factory(make_app: Callable, tmp_path: Path, request) -> Callable:
    """Return a factory builder pointing to the tmp directory."""

    def _func(src_folder: str, files: dict[str, str] | None = None, **kwargs) -> SphinxBuild:
        """Create the SphinxBuild from the source folder."""
        no_temp = environ.get("SST_TEST_HTML_DIR")
        nonlocal tmp_path
        if no_temp is not None:
            tmp_path = Path(no_temp) / request.node.name / str(src_folder)
        srcdir = tmp_path / src_folder
        copytree(tests_path / "sites" / src_folder, tmp_path / src_folder)
        for filename, contents in (files or {}).items():
            Path(srcdir / filename).resolve().write_text(contents)
        app = make_app(srcdir=srcdir, **kwargs)
        return SphinxBuild(app, tmp_path / src_folder)

    return _func


# -- global fixture to serve the built docs ----------------------------------


@pytest.fixture(scope="module")
def url_base():
    """Start local server on built docs and return the localhost URL as the base URL."""
    # The accessibility tests are run against a build of our documentation, so
    # fail early with a helpful message if it has not been built yet.
    if not docs_build_path.is_dir():
        msg = f"No docs build found at {docs_build_path}; build it first with 'tox -e build_docs'"
        pytest.fail(msg, pytrace=False)

    # Use a port that is not commonly used during development or else you will
    # force the developer to stop running their dev server in order to run the
    # tests.
    port = 8213
    host = "localhost"
    url = f"http://{host}:{port}"

    # Try starting the server
    process = Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", docs_build_path],
        stdout=PIPE,
    )

    # Try connecting to the server
    retries = 5
    while retries > 0:
        conn = HTTPConnection(host, port)
        try:
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response is not None:
                yield url
                break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1
        finally:
            conn.close()

    # If the code above never yields a URL, then we were never able to connect
    # to the server and retries == 0.
    if not retries:
        msg_0 = "Failed to start http server in 5 seconds"
        raise RuntimeError(msg_0)
    else:
        # Otherwise the server started and this fixture is done now and we clean
        # up by stopping the server.
        process.terminate()
        process.wait()

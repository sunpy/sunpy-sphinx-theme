"""Configuration of the pytest session."""

import sys
import time
from http.client import HTTPConnection
from pathlib import Path
from subprocess import PIPE, Popen

import pytest

repo_path = Path(__file__).parent.parent
docs_build_path = repo_path / "docs" / "_build" / "html"


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

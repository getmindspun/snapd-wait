import argparse
import os

from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

import pytest


path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "bin", "snapd-wait")
)

spec = spec_from_loader("script", SourceFileLoader("script", path))
script = module_from_spec(spec)
spec.loader.exec_module(script)


@pytest.fixture(scope="function", name="get_euid", autouse=True)
def get_euid_fixture(mocker):
    get_euid = mocker.patch("os.geteuid")
    get_euid.return_value = 0
    return get_euid


@pytest.fixture(scope="function", name="args")
def args_fixture():
    return argparse.Namespace(
        delay=script.DELAY,
        max_wait_time=script.MAX_WAIT_TIME,
        sleep=script.SLEEP,
        timeout=script.TIMEOUT
    )


@pytest.fixture(scope="function", name="script")
def script_fixture():
    return script

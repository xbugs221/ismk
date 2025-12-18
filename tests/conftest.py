import os
import sys
from contextlib import suppress
from pathlib import Path

import pytest

from ismk.common import ON_WINDOWS
from ismk.utils import find_bash_on_windows
from ismk.shell import shell

TEST_CACHE_BASE = Path(__file__).resolve().parent / ".cache"
TEST_CACHE_BASE.mkdir(exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(TEST_CACHE_BASE))

@pytest.fixture
def mocker():
    import unittest.mock as mock

    return mock

ON_MACOS = sys.platform == "darwin"
skip_on_windows = pytest.mark.skipif(ON_WINDOWS, reason="Unix stuff")
only_on_windows = pytest.mark.skipif(not ON_WINDOWS, reason="Windows stuff")
needs_strace = pytest.mark.xfail(
    os.system("strace -o /dev/null true") != 0, reason="Missing strace"
)


@pytest.fixture(autouse=True)
def reset_paths_between_tests():
    """Ensure that changes to sys.path are reset between tests"""
    org_path = sys.path.copy()
    yield
    sys.path = org_path


bash_cmd = find_bash_on_windows()

if ON_WINDOWS and bash_cmd:

    @pytest.fixture(autouse=True)
    def prepend_usable_bash_to_path(monkeypatch):
        monkeypatch.setenv("PATH", os.path.dirname(bash_cmd), prepend=os.pathsep)

    @pytest.fixture(autouse=True)
    def reset_shell_exec_on_windows(prepend_usable_bash_to_path):
        shell.executable(None)


@pytest.fixture
def s3_storage():
    from ismk.interfaces.common.plugin_registry.plugin import TaggedSettings

    try:
        from ismk_storage_plugin_s3 import StorageProviderSettings
        import boto3
    except ImportError:
        pytest.skip("s3 storage plugin is unavailable in this environment.")

    import uuid

    endpoint_url = "http://127.0.0.1:9000"
    access_key = "minio"
    secret_key = "minio123"
    bucket = f"ismk-{uuid.uuid4().hex}"

    try:
        boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        ).list_buckets()
    except Exception:
        pytest.skip("s3 endpoint is not reachable in this environment.")

    tagged_settings = TaggedSettings()
    tagged_settings.register_settings(
        StorageProviderSettings(
            endpoint_url=endpoint_url,
            access_key=access_key,
            secret_key=secret_key,
        )
    )

    yield f"s3://{bucket}", {"s3": tagged_settings}

    # clean up using boto3
    s3c = boto3.resource(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    with suppress(Exception):
        s3c.Bucket(bucket).delete()

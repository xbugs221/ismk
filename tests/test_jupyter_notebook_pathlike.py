import json
import shutil
from pathlib import Path

import pytest

from .common import run
from ismk.interfaces.executor_plugins.settings import DeploymentMethod

if shutil.which("conda") is None:
    pytest.skip("conda is not available in this environment.", allow_module_level=True)


# See https://github.com/ismk/ismk/pull/3636.
SNAKEFILE = """\
from pathlib import Path

DIR = Path("scripts")

rule all:
    conda: "env.yaml"
    notebook: DIR / "process_data.ipynb"
"""

ENV_YAML = """\
channels:
  - conda-forge
  - bioconda
dependencies:
  - python >=3.5
  - jupyter
  - papermill
"""

NOTEBOOK = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "cells": [],
    "metadata": {
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
    },
}


@pytest.fixture
def testdir(tmpdir):
    p = tmpdir.mkdir("testdir")
    p.mkdir("scripts")
    return p


@pytest.fixture
def testdir_notebook_pathlike(testdir):
    p = testdir.join("scripts", "process_data.ipynb")
    p.write(json.dumps(NOTEBOOK))
    p = testdir.join("env.yaml")
    p.write(ENV_YAML)
    p = testdir.join("Snakefile")
    p.write(SNAKEFILE)
    return testdir


def test_jupyter_notebook_pathlike(testdir_notebook_pathlike):
    run(
        Path(testdir_notebook_pathlike),
        check_results=False,
        deployment_method={DeploymentMethod.CONDA},
    )

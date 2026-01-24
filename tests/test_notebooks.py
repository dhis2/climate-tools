from pathlib import Path

import pytest
import papermill

SCRIPT_DIR = Path(__file__).parent.resolve()

GUIDES_DIR = (SCRIPT_DIR / "../docs/guides").resolve()
WORKFLOWS_DIR = (SCRIPT_DIR / "../docs/workflows").resolve()
OUTPUT_DIR = (SCRIPT_DIR / "outputs").resolve()
OUTPUT_DIR.mkdir(exist_ok=True)


# collect notebooks

GUIDES_NOTEBOOKS = list(GUIDES_DIR.rglob("*.ipynb"))
WORKFLOWS_NOTEBOOKS = list(WORKFLOWS_DIR.rglob("*.ipynb"))
ALL_NOTEBOOKS = GUIDES_NOTEBOOKS + WORKFLOWS_NOTEBOOKS


# ignore notebooks

SKIP_NOTEBOOKS = [
    "import-data-values.ipynb",
    "prepare-metadata.ipynb",
]

def ignore_notebook(nb):
    # ignore if
    if nb.name in SKIP_NOTEBOOKS:
        # hardcoded filenames to skip
        return True
    elif ".ipynb_checkpoints" in nb.parts:
        # just jupyter artifacts and backups
        return True
    elif "data" in nb.parts:
        # data folders should only contain static data files
        return True
    elif nb.name.startswith("_"):
        # unfinished notebooks
        return True
    else:
        # dont ignore
        return False

ALL_NOTEBOOKS = [nb for nb in ALL_NOTEBOOKS if not ignore_notebook(nb)]


# group notebooks

def is_slow(nb):
    if "getting-data" in nb.parts:
        # notebooks for downloading data
        return True
    elif "workflows" in nb.parts:
        # end-to-end import workflows
        return True
    else:
        # is not slow
        return False

SLOW_NOTEBOOKS = [nb for nb in ALL_NOTEBOOKS if is_slow(nb)]
FAST_NOTEBOOKS = [nb for nb in ALL_NOTEBOOKS if nb not in SLOW_NOTEBOOKS]


# the tests

@pytest.mark.parametrize("nb_path", FAST_NOTEBOOKS, ids=lambda nb: nb.name)
def test_fast_notebooks(nb_path, notebook_kernel):
    '''By default only run fast notebooks'''
    output_path = OUTPUT_DIR / f"{nb_path.stem}_out.ipynb"
    papermill.execute_notebook(
        str(nb_path), 
        str(output_path), 
        cwd=str(nb_path.parent),
        kernel_name=notebook_kernel,
    )

@pytest.mark.skip
@pytest.mark.parametrize("nb_path", SLOW_NOTEBOOKS, ids=lambda nb: nb.name)
def test_slow_notebooks(nb_path, notebook_kernel):
    '''
    Slow notebooks can only be run if manually specified,
    eg pytest tests/test_notebooks.py::test_slow_notebooks.
    However, this may not work yet, since they require setting 
    an element id that doesn't exist on the play server.
    Could be nice to fix this in the future, maybe auto create metadata.
    '''
    output_path = OUTPUT_DIR / f"{nb_path.stem}_out.ipynb"
    papermill.execute_notebook(
        str(nb_path), 
        str(output_path), 
        cwd=str(nb_path.parent),
        kernel_name=notebook_kernel,
    )

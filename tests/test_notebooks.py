from pathlib import Path
from itertools import groupby

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
    #"import-data-values.ipynb",
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
        # don't ignore
        return False

ALL_NOTEBOOKS = [nb for nb in ALL_NOTEBOOKS if not ignore_notebook(nb)]


# group notebooks

def notebook_type(nb):
    if "getting-data" in nb.parts:
        # notebooks for downloading data
        return "data_download"
    elif "workflows" in nb.parts:
        # end-to-end import workflows
        return "full_import"
    else:
        # fast
        return "fast"

notebook_groups = {
    notebook_type: list(notebooks)
    for notebook_type,notebooks
    in groupby(sorted(ALL_NOTEBOOKS, key=notebook_type), key=notebook_type)
}


# the tests

@pytest.mark.parametrize("nb_path", notebook_groups["fast"], ids=lambda nb: nb.name)
def test_fast_notebooks(nb_path, notebook_kernel):
    '''By default only run fast notebooks'''
    output_path = OUTPUT_DIR / f"{nb_path.stem}_out.ipynb"
    papermill.execute_notebook(
        str(nb_path), 
        str(output_path), 
        cwd=str(nb_path.parent),
        kernel_name=notebook_kernel,
    )

@pytest.mark.integration
@pytest.mark.parametrize("nb_path", 
                         notebook_groups["data_download"] + notebook_groups["full_import"], 
                         ids=lambda nb: nb.name)
def test_integration_notebooks(nb_path, notebook_kernel):
    '''
    Slow notebooks are marked as integration and are only run if 
    manually specified, eg pytest -m integration.
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

@pytest.mark.integration
@pytest.mark.data_download
@pytest.mark.parametrize("nb_path", 
                         notebook_groups["data_download"],
                         ids=lambda nb: nb.name)
def test_data_download_notebooks(nb_path, notebook_kernel):
    '''
    Only the data download subset of integration tests.
    Run with pytest -m "integration and data_download"
    '''
    output_path = OUTPUT_DIR / f"{nb_path.stem}_out.ipynb"
    papermill.execute_notebook(
        str(nb_path), 
        str(output_path), 
        cwd=str(nb_path.parent),
        kernel_name=notebook_kernel,
    )

@pytest.mark.integration
@pytest.mark.full_import
@pytest.mark.parametrize("nb_path", 
                         notebook_groups["full_import"],
                         ids=lambda nb: nb.name)
def test_full_import_notebooks(nb_path, notebook_kernel):
    '''
    Only the full import workflow subset of integration tests.
    Run with pytest -m "integration and full_import"
    '''
    output_path = OUTPUT_DIR / f"{nb_path.stem}_out.ipynb"
    papermill.execute_notebook(
        str(nb_path), 
        str(output_path), 
        cwd=str(nb_path.parent),
        kernel_name=notebook_kernel,
    )

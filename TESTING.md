# Testing

To ensure that the notebooks are always working, we use [pytest](https://docs.pytest.org/en/stable/) to execute and verify that the notebooks don't unexpectedly break. 

The notebooks are automatically executed using the [tests GitHub Action](.github/workflows/tests.yml) on pushes and pull requests
to the `main` branch. Notebooks are run across all [supported Python versions](docs/getting-started/installation.md#supported-python-versions) to ensure compatibility and reproducibility.

In this document you will find details on how the tests work, and how to run the tests locally. 

## About Notebook Tests

- Tests are in `tests/test_notebooks.py`
- Notebooks are discovered recursively in `docs/` while ignoring some files.
- Notebooks are executed using [papermill](https://papermill.readthedocs.io/en/latest/index.html) and requires specifying the environment/kernel name. 
- Output notebooks are written to `tests/outputs/` (ignored by git).

## What you need

1. To run the tests locally, you need a working environment of the DHIS2 Climate Tools. See the [installation instructions](docs/getting-started/installation.md). 

2. After setting up your environment for the first time, make sure you have registered the environment as a Jupyter kernel:

    ```bash
    python -m ipykernel install --user --name <name-of-env>
    ```

## Running Tests

By default `pytest` only runs `fast` notebooks that primarily loads data from files in `data` folder:

```bash
pytest --notebook-kernel=<name-of-env> -vv
```

To run integration tests for data downloads (reuses cache if previously downloaded):

```bash
pytest -m "integration and data_download" --notebook-kernel=<name-of-env> -vv
```

To run integration tests for full import workflows (requires creating and setting data element ids first):

```bash
pytest -m "integration and full_import" --notebook-kernel=<name-of-env> -vv
```

To run all the integration tests:

```bash
pytest -m integration --notebook-kernel=<name-of-env> -vv
```

After testing, executed copies of notebooks are written to `tests/outputs/` for inspection and debugging only; these output notebooks are not intended to be re-run. 

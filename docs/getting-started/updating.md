---
title: Staying up to date
---

DHIS2 Climate Tools is a continuously evolving toolkit. The `main` branch of the [Github repository](https://github.com/dhis2/climate-tools) always reflects the latest recommended version, including the notebooks shown on the [website](https://climate-tools.dhis2.org/).

To stay up to date with the latest changes, follow the steps on this page. This involves replacing your local copy with the latest version from the repository and updating your Python environment.

The most recent changes can be viewed in the [GitHub commit history](https://github.com/dhis2/climate-tools/commits/main).

## Important: local changes will be lost

The DHIS2 Climate Tools repository is **not** intended to store your own work.

- Notebooks are provided as guides and reference workflows to explore.
- Any local modifications to notebooks or files inside the repository will be overwritten or lost when you update.
- If you want to keep your own analyses or experiments, copy notebooks to a separate directory outside the repository.

## Updating your local installation

From inside the repository:

```bash
git fetch
git reset --hard origin/main
pip install --upgrade -r requirements.txt
```

This will:

- Discard local changes in the repository
- Update notebooks to the latest versions
- Ensure your environment matches the current documentation

## If something goes wrong

If you encounter dependency issues or unexpected errors after updating, the safest option is to: 

- Deactivate and remove your old environment: 

    ```bash
    conda deactivate
    conda env remove -n climate-tools
    ```

- Recreate the environment following the [installation](installation.md) instructions. 

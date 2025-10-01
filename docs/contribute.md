# How to contribute

This page describes guidelines if you're a developer or want to contribute back to Climate Tools.  

## Developer setup

If you're a developer who wants to contribute to Climate Tools, we recommend fetching the latest main branch on Github and installing directly from source (development mode): 

        $ git clone https://github.com/dhis2/climate-tools.git
        $ cd climate-tools
        $ pip install -e .

Once installed, you can verify that they installed correctly:

- the Python library:

    ```python
    import dhis2eo
    ```

- the CLI tool:

        $ dhis2eo --help

  If you're on Windows, the above command may not work due to a bug with `pip install -e`. Instead try:

        $ python -m dhis2eo --help

## Code contributions

If you have code contributions:

- Fork or create a new branch of the [Climate Tools Github repo](https://github.com/dhis2/climate-tools).
- Make your changes inside the relevant parts of the `dhis2eo` folder. 
- If adding new functionality, add a Jupyter Notebook file that demonstrates how to use the new code (see next section on [Jupyter Notebooks](#notebook-contributions)). 
- Push your changes and make a **Pull Request** to the `main` branch. 

## Notebook contributions

We also welcome user-contributions from practitioners and others who have developed useful scripts or workflows showcasing how to execute common climate operations and workflows. In these cases we ask that you create this as an interactive Jupyter Notebook that guides others through the workflow, executes code, and visualizes results if relevant. 

Here's a step-by-step guide:

1. Create your own fork of the latest [Climate Tools Github repo](https://github.com/dhis2/climate-tools).

2. Write your Jupyter Notebook. 
    - See our guide for [Getting started with Jupyter](getting-started/jupyter.md). 
    - Place your notebook file in the relevant section of the documentation, e.g. `docs/aggregation`.
    - Make sure that all relevant data files are added to the `docs/data` folder, or retrieved from online sources. 
    - Run all cells in your notebook before submitting to verify that everything works and the outputs are up-to-date. 

3. Add your notebook to the documentation page tree. 
    - Open the file `docs/myst.yml` - this defines the structure of the online documentation and the pages shown in the side menu. 
    - Add an entry to your notebook in the relevant section (alternatively, suggest a new section):

        ```
        - title: Data aggregation
          children:
              - file: aggregation/your-custom-notebook.ipynb
        ```

4. Preview the updated website locally.
    - The online documentation is built using Jupyter Book (https://next.jupyterbook.org). 
    - To preview the documentation locally you need to install Jupyter Book v2: 

            $ pip install --pre "jupyter-book==2.\*"

    - After installing the dependencies you have to first navigate to the `docs` folder:

            $ cd docs

    - Then run the Jupyter server locally:

            $ jupyter book start

    - Visit localhost:3000 to preview your local changes. 

5. Finally, push your changes and make a **Pull Request** back to the [Climate Tools Github repo](https://github.com/dhis2/climate-tools). 
    - Once the PR is accepted, the site at https://dhis2.github.io/climate-tools/ will be automatically updated. 
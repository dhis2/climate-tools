# Climate Tools

Site: https://dhis2.github.io/climate-tools

## Installation

To install the climate tools Python library, and its associated commandline utilities, you need to install the `climtools` Python package. 

Until we release an official PyPI package, for now you can simply install it from the github repository:

        $ pip install git+https://github.com/dhis2/climate-tools

Or if you're a developer, install your local repository in editable mode, so that local changes get reflected during import:

        $ pip install -e .

After this, you should be able to import `climtools` inside a Python session:

        >>> import climtools
        
Installation will also make available the Climtools CLI from the commandline: 

        $ climtools

## Documentation

The climate tools documentation also includes a number of guides and examples for common climate operations and workflows, available at https://dhis2.github.io/climate-tools. This online documentation is built using the MyST web publishing ecosystem (https://mystmd.org/guide/quickstart) and Jupyter v2 (https://next.jupyterbook.org). The site is automatically updated by making changes to the `docs` folder and pushing to the `main` branch. 

To preview the documentation locally you need to have `Node.js` (https://nodejs.org) installed. Additionally you need to install the following Python packages: 

        $ pip install mystmd
        $ pip install --pre "jupyter-book==2.\*"

After installing the dependencies you can run the web server locally:

        $ jupyter book start

You can then browse and preview your local changes:

- Visit localhost:3001 in your browser

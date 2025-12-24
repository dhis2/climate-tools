---
title: Installation
---


## Download the notebooks

All the tutorials and workflows from the [DHIS2 Climate Tools website](https://climate-tools.dhis2.org/) are available as interactive Jupyter notebooks inside the [DHIS2 Climate Tools GitHub repository](https://github.com/dhis2/climate-tools). To run these notebooks on your local computer, you first have to git clone the repository:

    git clone https://github.com/dhis2/climate-tools


## Choose a version branch

The DHIS2 Climate Tools is updated periodically to include new resources or bug fixes. Each version of the toolkit is pinned to specific dependencies to ensure reproducibility. 

To make sure you are running a stable tested version of the toolkit, checkout the specific version branch that you want to explore, e.g.:

    git checkout v2025.1

Below is a list of available version branches that you can checkout:

- **v2025.1** – Python 3.10 (not released yet)


## Install the necessary dependencies

To setup the necessary environment required to run the DHIS2 Climate Tools tutorials and workflows, you can write:

    pip install -r requirements.txt


## Running the notebooks

Now you should have what you need to run the Jupyter notebooks. See our [guide for getting started with Jupyter](jupyter.md). 

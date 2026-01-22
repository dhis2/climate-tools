---
title: Installation
---


## Prerequisites

Before you get started with DHIS2 Climate Tools, make sure you have the following installed:

- [Git](https://git-scm.com/) – for cloning repositories and managing updates.
- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) for managing a reproducible Python environment.
    - Follow the [installation instructions](https://www.anaconda.com/docs/getting-started/miniconda/install).
    - Run `conda init --all` in your terminal.
    - Restart your terminal for the changes to take effect.

The installation instructions on this page have only been tested to work on **Python 3.11**.

## Download the DHIS2 Climate Tools toolkit

DHIS2 Climate Tools is available as a [single GitHub repository](https://github.com/dhis2/climate-tools), which contains:

- A ready-to-use Python environment to get you started working with climate data and DHIS2
- A set of How-to Guides and Reference Workflows as interactive Jupyter notebooks for learning and exploration, which are the same notebooks published on the [website](https://climate-tools.dhis2.org/)

To download the toolkit to your local machine, clone the repository:

    git clone https://github.com/dhis2/climate-tools

The DHIS2 Climate Tools is updated on a continuous basis to update the notebooks and reference environment. 

## Setup the environment

First, use `conda` create and activate the Python environment:

    conda create -n climate-tools python=3.11
    conda activate climate-tools

Install the dependencies in this order:

    conda install pymeeus
    conda install -c conda-forge jupyterlab ipywidgets jupyterlab_widgets
    pip install -r requirements.txt

## Running the notebooks

You’re now ready to explore the included How-to Guides and Reference Workflows.

For help getting started with Jupyter Notebooks, see our [Jupyter guide](jupyter.md).

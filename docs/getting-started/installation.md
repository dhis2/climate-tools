---
title: Installation
---


## Prerequisites

Before you get started with DHIS2 Climate Tools, make sure you have the following installed:

- [Git](https://git-scm.com/) – for cloning repositories and managing updates
- Python ≥ 3.10 (provided either by Miniconda or a system Python installation)
    - Recommended: [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) for managing a reproducible Python environment

## Download the DHIS2 Climate Tools toolkit

DHIS2 Climate Tools is available as a [single GitHub repository](https://github.com/dhis2/climate-tools), which contains:

- A ready-to-use Python environment to get you started working with climate data and DHIS2
- A set of How-to Guides and Reference Workflows as interactive Jupyter notebooks for learning and exploration, which are the same notebooks published on the [website](https://climate-tools.dhis2.org/)

To download the toolkit to your local machine, clone the repository:

    git clone https://github.com/dhis2/climate-tools

The DHIS2 Climate Tools is updated on a continuous basis to update the notebooks and reference environment. 

## Setup the environment

If you are using Miniconda, create and activate a new environment, for example:

    conda create -n climate-tools python=3.13
    conda activate climate-tools

Next, install the required dependencies:

    pip install -r requirements.txt


## Running the notebooks

You’re now ready to explore the included How-to Guides and Reference Workflows.

For help getting started with Jupyter Notebooks, see our [Jupyter guide](jupyter.md).

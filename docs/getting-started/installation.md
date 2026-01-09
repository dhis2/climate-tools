---
title: Installation
---


## Prerequisites

Before you get started with DHIS2 Climate Tools, make sure you have the following installed:

- [Git](https://git-scm.com/) – for cloning repositories and managing updates
- Optional: [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) – recommended for managing a reproducible Python environment


## Download the DHIS2 Climate Tools toolkit

DHIS2 Climate Tools is available as a [single GitHub repository](https://github.com/dhis2/climate-tools), which contains:

- A ready-to-use Python environment to get you started working with climate data and DHIS2
- All How-to Guides and Reference Workflows from the [website](https://climate-tools.dhis2.org/) as interactive Jupyter notebooks

To download the toolkit to your local machine, clone the repository:

    git clone https://github.com/dhis2/climate-tools


## Choose a release version

The DHIS2 Climate Tools is updated periodically to include new resources or bug fixes. Each release version of the toolkit is pinned to specific dependencies to ensure reproducibility. 

See all available releases on GitHub: [DHIS2 Climate Tools Releases](https://github.com/dhis2/climate-tools/releases)

For example, to checkout release v2026.1:

    git fetch --tags
    git checkout v2026.1


## Setup the environment

Make sure your Python version matches the version of the toolkit you are using (check the `python-version.txt` file in the release to see which Python version to use). 

If you are using Miniconda, create and activate a new environment. For example, if your version of DHIS2 Climate Tools requires Python 3.10:

    conda create -n climate-tools python=3.10
    conda activate climate-tools

Next, install the required dependencies:

    pip install -r requirements.txt


## Running the notebooks

You’re now ready to explore the included How-to Guides and Reference Workflows, or create your own Jupyter notebooks for climate and health data workflows.

For help getting started with Jupyter Notebooks, see our [Jupyter guide](jupyter.md).

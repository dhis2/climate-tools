---
title: Jupyter Notebooks
---

Some of the documentation on the Climate Tools website also functions as interactive Jupyter Notebooks that can be used as learning material. This guide shows how to get started exploring and running these notebooks for yourself. 

In this tutorial we specifically show how to use the classical Jupyter interface, but it's also possible to use any preferred tool such as the [VSCode Jupyter notebook extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter). 

## Installing Jupyter

Jupyter can be installed with:

        $ pip install jupyter



## Download the Climate Tools Notebooks

The notebooks are located inside the `docs` folder of the [Climate Tools repository](https://github.com/dhis2/climate-tools). 

Clone the main repository to your local computer:

        $ git clone https://github.com/dhis2/climate-tools

Alternatively you can download the latest code as a zipfile from this link: https://github.com/dhis2/climate-tools/archive/refs/heads/main.zip

## Start the Jupyter Server

Start the Jupyter server at the root of the downloaded repository folder, which will give you an overview of the folder contents.

        $ cd path/to/local/repo
        $ jupyter notebook

**Note**: It's important that `jupyter` and `dhis2eo` are installed to the same virtual environment (e.g. in `venv` or `conda`), and that you activate this environment before you run `jupyter notebook`. This will ensure that Jupyter uses the correct Python version with all the necessary dependencies installed. 

## Browse the Notebooks

Visit http://localhost:8888, which will give you an overview of the folder contents. 

Browse the `docs` folder and look for files with `.ipynb` extensions. For instance, if you navigate to the `docs/aggregation` folder you'll find the `earthkit-netcdf.ipynb` file: 

![Screenshot of browsing files in Jupyter](./images/jupyter-browse.png)

----------------------------------

## Open and run a notebook

Click one of the notebooks to open it: 

![Screenshot of a Jupyter Notebook](./images/jupyter-notebook.png)

We recommend running the notebook step by step, which you can do by clicking each individual code cell and pressing control-enter to run it. Then you'll see the results of each code cell as you go through the document. 

## Next steps

In this tutorial we have shown how to get started with the notebooks already provided in the Climate Tools repository. 

You can also create your own notebooks for exploring data or executing common workflows. We aim to gather a collection of user-contributed notebooks for useful climate and health workflows:

- Visit the [How to Contribute page](../contribute.md) for help on how to contribute your notebooks.

For more information on how to use Jupyter Notebooks you can check out this tutorial: 

- https://www.dataquest.io/blog/jupyter-notebook-tutorial/. 

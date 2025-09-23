---
title: Jupyter Notebooks
---

In addition to using the Python package in your scripts and favorite IDE, you also have the option to use Jupyter Notebooks to run your code more interactively. 

This repository includes some notebooks that can be used as example workflows or templates inside the `docs` folder. But it's up to you to create your own Notebooks for your own use-case. 

## Installing Jupyter

Jupyter can be installed with:

        $ pip install jupyter

## Running the server

After installation, you can navigate to the folder where you want to store your Notebooks, and start a Jupyter Notebook server:

        $ cd path/to/workspace/folder
        $ jupyter notebook

You can then visit http://localhost:8888 to view, create, and run Jupyter notebooks in the selected workspace. 

### Example usage

For instance, if you start the Jupyter server in this repository folder and navigate to the `docs/aggregation` folder you'll find the `earthkit-netcdf.ipynb` file: 

![Screenshot of browsing files in Jupyter](./images/jupyter-browse.png)

Click it to open the notebook: 

![Screenshot of a Jupyter Notebook](./images/jupyter-notebook.png)

For instance, we recommend running the notebook step by step, which you can do by clicking each individual code cell and pressing control-enter to run it. Then you'll see the results of each code cell as you go through the document. 

For more information on how to use Jupyter Notebooks you can check out this tutorial: https://www.dataquest.io/blog/jupyter-notebook-tutorial/. 
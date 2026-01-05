---
title: How to contribute
short_title: Contribute
---

This page describes guidelines if you're a developer and want to contribute back to the DHIS2 Climate Tools. 


## Share your use case

We advise you to start by adding a new topic in this category of our Community of Practice: [Development > Climate Tools](https://community.dhis2.org/c/development/climate-tools/93). Describe what you want to achieve, and how you plan to implement it. This will allow us to have a discussion around the topic, which tools to use, and how we can make it generic and reusable to benefit our community. After this initial discussion you should be ready to start with the implementation.


## Notebook contributions

We want DHIS2 Climate Tools to be a collaborative collection of user-contributed example workflows in the form of Jupyter notebooks, e.g. if you have developed useful scripts or workflows showcasing how to execute common climate operations and workflows. In these cases we ask that you create this as an interactive Jupyter Notebook that takes the reader through the workflow, executes code, and visualizes results if relevant.

Here's a step-by-step guide:

1. Create a fork of the latest [DHIS2 Climate Tools Github repo](https://github.com/dhis2/climate-tools) to your own GitHub account. 

2. Clone the forked repo to your local computer: 

        git clone https://github.com/<your-username>/climate-tools

3. Follow our [guide to setup the necessary environment](getting-started/installation.md). 

4. Write your Jupyter Notebook.

    - See our guide for [Getting started with Jupyter](getting-started/jupyter.md).
    - Place your notebook file in a new folder inside the `examples` folder of the documentation, e.g. `docs/examples/your-folder`.
    - Make sure that all relevant data files are included in your example folder, or retrieved from online sources.
        - **Important:** Make sure that the files are not very large (>50MB) and does not contain sensitive or private data. 
    - Run all cells in your notebook before submitting to verify that everything works and the outputs are up-to-date.

5. Add your notebook to the documentation page tree.

    - Open the file `docs/toc.yml` - this defines the structure of the online documentation and the pages shown in the side menu.
    - Add an entry linking to your notebook in the Examples section:

      ```
    - title: Examples
      children:
        ...
        - file: examples/your-folder/your-custom-notebook.ipynb
      ```

6. Preview the updated website locally.

    - The online documentation is built using Jupyter Book (https://next.jupyterbook.org).
    - To preview the documentation locally you need to install Jupyter Book v2:

            pip install --pre "jupyter-book==2.\*"

    - After installing the dependencies you have to first navigate to the `docs` folder:

            cd docs

    - Then run the Jupyter server locally:

            jupyter book start

    - Visit localhost:3000 to preview your local changes.

7. Make your commits and push your changes. 

        git commit -m "Description of your changes..."
        git push

8. Finally, [create a Pull Request (PR) from your forked repository](https://github.com/dhis2/climate-tools/compare) back to the DHIS2 Climate Tools Github repo. 

9. Follow along the conversation on your PR, and make any requested changes.  

10. Once the PR is accepted, your contribution will be included as part the DHIS2 Climate Tools collection of workflows at [climate-tools.dhis2.org](climate-tools.dhis2.org) the next time we release a new version. 


## Code contributions

We also welcome code contributions to any of the libraries that we develop and maintain: 

- [dhis2eo](https://climate-tools.dhis2.org/tools/dhis2eo/)
- [dhis2-python-client](https://github.com/dhis2/dhis2-python-client)

# Copilot Instructions for DHIS2 Climate Tools

## Project Overview

DHIS2 Climate Tools is a documentation and tutorial project that helps users integrate climate, weather, and environmental data with DHIS2 (a health information system) and the Chap Modeling Platform. The project focuses on **documentation in the `docs/` folder**, which is built as a Jupyter Book 2 website.

**Important:** The `dhis2eo` Python package folder is planned to be moved to a separate repository in the future. For now, focus all work on the documentation in the `docs/` folder.

### Key Purpose
- Provide tutorials and workflows for climate-health data integration
- Teach data engineers to build automated data pipelines
- Guide data scientists on analyzing climate data with Python
- Document best practices using earthkit, DHIS2 APIs, and Python geospatial tools

## Technology Stack

### Documentation Platform
- **Jupyter Book 2** (MyST Markdown): Modern documentation framework
- **MyST Markdown**: Enhanced Markdown with special directives
- **Node.js**: Required to run Jupyter Book
- Package manager: npm

### Python Ecosystem
- **Python 3.11+**: Recommended version
- **earthkit**: Climate data access and processing (from ECMWF)
  - `earthkit-data`: Data loading from various sources
  - `earthkit-transforms`: Spatial/temporal aggregation
  - `earthkit-plots`: Visualization
- **dhis2-python-client**: DHIS2 Web API integration
- **Jupyter Notebooks**: Interactive tutorials (`.ipynb` files)
- **GeoPandas/Xarray**: Geospatial and multidimensional data handling

### Data Sources
- Climate Data Store (CDS) - ERA5 reanalysis data
- WorldPop - Population data
- DHIS2 - Organization unit boundaries and health data

## Repository Structure

```
climate-tools/                     # Repository root
├── docs/                          # Main documentation folder (FOCUS HERE)
│   ├── myst.yml                   # Table of contents and site configuration
│   ├── package.json               # Node dependencies for Jupyter Book
│   ├── index.md                   # Homepage
│   ├── about.md                   # Project information
│   ├── getting-started/           # Installation and setup guides
│   ├── tools/                     # Tool descriptions (earthkit, dhis2eo, etc.)
│   ├── users/                     # User personas (data engineer, data scientist)
│   ├── org-units/                 # DHIS2 organization unit tutorials
│   ├── getting-data/              # Data download tutorials
│   │   ├── climate-data-store/    # ERA5 data tutorials
│   │   └── worldpop/              # Population data tutorials
│   ├── analysis/                  # Data analysis examples
│   ├── visualization/             # Plotting and visualization
│   ├── aggregation/               # Spatial/temporal aggregation
│   ├── import-data/               # DHIS2 data import tutorials
│   ├── data/                      # Sample data files for notebooks
│   ├── images/                    # Documentation images
│   ├── parts/                     # Reusable page components
│   └── _unused/                   # Deprecated/archived content
├── dhis2eo/                       # Python package (will be moved - ignore)
├── tests/                         # Python tests
├── pyproject.toml                 # Python package config
├── .github/workflows/deploy.yml   # GitHub Pages deployment
└── README.md                      # Project README
```

## Working with Documentation

### Site Configuration (`docs/myst.yml`)
- **Critical file**: Defines the entire site structure and navigation
- `project.toc`: Table of contents - controls sidebar navigation order
- `site.template`: Set to `book-theme` for book-style layout
- `site.nav`: Top navigation bar links
- When adding new pages, **always update the `toc` section** to include them

### MyST Markdown Features
MyST extends standard Markdown with special directives:

```markdown
# Standard Markdown works
Use headings, lists, links, images normally

# Special MyST directives
:::{note}
This is a note admonition
:::

:::{figure} ./images/example.png
:alt: Alt text
Caption text
:::

:::{glossary}
Term
: Definition
:::

{button}`Button text <./link>`
```

### Jupyter Notebooks (`.ipynb`)
Notebooks are the primary way to create interactive tutorials:

**Best Practices:**
1. **Always run all cells before committing** - outputs should be current
2. **Include frontmatter in first cell:**
   ```markdown
   ---
   title: Full Page Title
   short_title: Sidebar Title
   ---
   ```
3. **Use sample data from `docs/data/`** - keep data files small
4. **Add narrative text cells** - explain what's happening, don't just show code
5. **Keep notebooks focused** - one clear workflow per notebook
6. **Import libraries in first code cell:**
   ```python
   import geopandas as gpd
   import earthkit.data
   from earthkit import transforms
   from dhis2eo.integrations.pandas import dataframe_to_dhis2_json
   ```

**Common Notebook Patterns:**
- Load data with `earthkit.data.from_source()`
- Aggregate with `earthkit.transforms.aggregate`
- Convert to DataFrame for DHIS2 with `dataframe_to_dhis2_json()`
- Visualize with matplotlib or earthkit-plots

### Adding New Content

**To add a new page:**
1. Create the `.md` or `.ipynb` file in the appropriate folder
2. **Update `docs/myst.yml`** in the `project.toc` section:
   ```yaml
   - title: Section Name
     file: section/intro.md
     children:
       - file: section/your-new-page.md
       - file: section/your-notebook.ipynb
   ```
3. Preview locally (see below)
4. Commit both the new file and updated `myst.yml`

**To add sample data:**
- Place in `docs/data/` folder
- Keep files small (< 10MB) when possible
- Use relative paths: `../data/filename.nc`
- Document data source and format in the notebook

### Building and Previewing

**Local preview workflow:**
```bash
# From repository root, navigate to docs folder
cd docs

# Install Jupyter Book (if not already installed)
npm install

# Start the development server
npm start
# or: jupyter-book start

# Visit http://localhost:3000 in browser
```

**Production build:**
```bash
cd docs
jupyter-book build --html
# Output in docs/_build/html/
```

**Automatic deployment:**
- Pushes to `main` branch trigger `.github/workflows/deploy.yml`
- Site deploys to GitHub Pages at https://dhis2.github.io/climate-tools/

### Linting and Code Quality

**No formal linters for documentation**, but follow these guidelines:
- Use consistent heading hierarchy (don't skip levels)
- Check internal links work (especially after moving files)
- Ensure all images have alt text
- Keep line lengths reasonable in Markdown files
- Use MyST directives consistently

**For Python code in notebooks:**
- Follow PEP 8 style
- Add docstrings to functions
- Use meaningful variable names
- Comment complex operations

## Common Workflows

### Climate Data Integration Tutorial
Typical workflow shown in notebooks:
1. **Get organization units** from DHIS2 as GeoJSON
2. **Download climate data** from Climate Data Store (NetCDF format)
3. **Load data** with earthkit-data
4. **Aggregate spatially** to organization units with earthkit-transforms
5. **Aggregate temporally** (e.g., daily to monthly means)
6. **Convert to DHIS2 format** with dhis2eo utilities
7. **Upload to DHIS2** via Web API

### Testing Strategy
**Currently minimal test infrastructure** for documentation:
- Primary "test": Build the Jupyter Book without errors
- Manual verification: Preview locally and check pages render correctly
- Notebook validation: Ensure all cells run without errors
- No automated tests needed for documentation changes

**If modifying Python code** (dhis2eo - though this will move):
- Tests in `tests/` folder use standard Python unittest/pytest
- Run with: `python -m pytest tests/`

## Key Concepts and Terminology

- **Organisation unit**: DHIS2 term for geographic regions (e.g., districts, health facilities)
- **NetCDF**: Standard format for climate/weather data (multi-dimensional arrays)
- **ERA5**: High-quality climate reanalysis dataset from ECMWF
- **Aggregation**: Converting high-resolution gridded data to regional averages
- **Period type**: DHIS2 time formats (daily, monthly, yearly)
- **Data element**: DHIS2 term for a specific variable/indicator
- **earthkit**: Suite of Python tools for climate data workflows

## Common Pitfalls and Solutions

### Problem: Notebook cells fail to execute
- Ensure sample data files exist in `docs/data/`
- Check that imports match available packages
- Verify data file paths use correct relative paths (`../data/...`)

### Problem: Page doesn't appear in sidebar
- Check that file is listed in `docs/myst.yml` under `project.toc`
- Ensure indentation is correct (YAML is indent-sensitive)
- Verify file path matches actual location

### Problem: Build fails with MyST errors
- Check for unclosed directives (`:::` must close each block)
- Verify YAML frontmatter is valid (in notebooks and .md files)
- Look for special characters that need escaping

### Problem: Images don't display
- Use relative paths from the current file location
- Check image file actually exists at that path
- Add to `docs/images/` folder if site-wide asset
- MyST syntax: `![alt text](./path/to/image.png)` or `:::{figure}` directive

### Problem: Links break after reorganizing content
- Update all internal links when moving files
- Use relative paths: `[text](../other-folder/page.md)`
- Update `myst.yml` if file paths change

## Contribution Guidelines

1. **Start with discussion**: Post in [DHIS2 Community forum](https://community.dhis2.org/c/development/climate-tools/93)
2. **Focus on generic workflows**: Make tutorials reusable across countries/contexts
3. **Include working examples**: Use small sample data that others can download
4. **Test notebooks thoroughly**: Run all cells before submitting
5. **Update table of contents**: Don't forget `docs/myst.yml`
6. **Follow existing style**: Match the tone and structure of existing pages
7. **Add to appropriate section**: Getting data, analysis, visualization, etc.

## Development Environment Setup

**For documentation work:**
```bash
# Clone repository
git clone https://github.com/dhis2/climate-tools.git
cd climate-tools/docs

# Install Node.js dependencies
npm install

# Start development server
npm start
```

**For Python package work (will move to separate repo):**
```bash
# Install in development mode
pip install -e .

# Install with all dependencies
pip install git+https://github.com/dhis2/climate-tools
```

## External Resources

- **Jupyter Book docs**: https://next.jupyterbook.org (note: using v2, not v1)
- **MyST Markdown**: https://mystmd.org/guide
- **earthkit website**: https://ecmwf.github.io/earthkit-website/
- **DHIS2 docs**: https://docs.dhis2.org/
- **DHIS2 for Climate & Health**: https://dhis2.org/climate/
- **Community forum**: https://community.dhis2.org/c/development/climate-tools/93

## Quick Reference

### Essential Commands
```bash
cd docs/                 # Always work from docs folder
npm install              # Install dependencies
npm start                # Preview locally
jupyter-book build --html  # Build static site
```

### Essential Files
- `docs/myst.yml` - Site structure and TOC (update when adding pages)
- `docs/index.md` - Homepage
- `docs/package.json` - Node dependencies

### Common MyST Directives
- `:::{note}`, `:::{warning}`, `:::{tip}` - Admonitions
- `:::{figure}` - Images with captions
- `:::{glossary}` - Term definitions
- `{button}` - Styled buttons/links
- `:::{iframe}` - Embed videos/external content

### Notebook Guidelines
1. Add frontmatter in first cell
2. Import all libraries upfront
3. Use sample data from `docs/data/`
4. Add explanatory text between code cells
5. Run all cells before committing
6. Update `myst.yml` to include the notebook

---

**Remember**: This project is about documentation and tutorials. Focus on creating clear, working examples that teach users how to integrate climate data with DHIS2. The goal is to help data engineers and data scientists succeed with climate-health data workflows.

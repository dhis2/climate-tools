---
title: "Scheduling data imports into DHIS2"
short_title: "Scheduling data imports"
---

This guide explains how to set up automated, scheduled imports of climate data into DHIS2. We demonstrate how to do this using the [Import ERA5-Land Daily](https://climate-tools.dhis2.org/workflows/import-era5/import-era5-daily/) workflow, showing how to move from interactive notebook exploration to production-ready scheduled imports. But the same approach can be used to setup a workflow for any other workflow or script. 

The key technologies we will use are [Docker](https://www.docker.com/) as a container to run the schedule, [cron](https://en.wikipedia.org/wiki/Cron) as the actual scheduling program, and [papermill](https://papermill.readthedocs.io/) to run the import notebook. 

For a complete example of an implementation that imports ERA5-Land data on a schedule, with additional convenience funcionality, see the [dhis2-era5land-simple](https://github.com/mortenoh/dhis2-era5land-simple) repository. 

## Prerequisites

Before starting, ensure you have:

- Completed the [CDS API Authentication](../../guides/getting-data/climate-data-store/api-authentication.md) setup
- Login credentials to a DHIS2 instance
    - Must include a data element for daily ERA5-Land temperature (see [Prepare Metadata](../../guides/import-data/prepare-metadata.ipynb))
- An installation of [Docker Desktop](https://www.docker.com/)
    - Also verify that Docker Desktop is actually running. 
- A basic familiarity with [the workflow for importing ERA5-Land data](../../workflows/import-era5/import-era5-daily.ipynb) which we are going to be automating. 

## 1) Gather the needed files

For this tutorial, we are going to be using the provided [example](https://github.com/dhis2/climate-tools/tree/main/docs/workflows/scheduling/example) folder. This folder contains all the files we'll be needing, and will be explained in more detail later. 

```bash
    workflows/
    └── scheduling/
        └── example
            ├── Dockerfile
            ├── docker-compose.yml
            ├── cronfile
            ├── requirements.txt  (copied from root folder)
            ├── notebooks
            |   └── import-era5-daily.ipynb  (copied from workflows folder)
            ├── configs
            |   └── import-temperature-config.yaml
            └── data
                └── ... (this is where climate data will be downloaded and cached)
```

Note that we have copied the `requirements.txt` file and the `import-era5-daily.ipynb` file from elsewhere in the repo. 

## 2) Make the notebook configurable

The [Import ERA5-Land Daily](https://climate-tools.dhis2.org/workflows/import-era5/import-era5-daily/) notebook hardcodes all input parameters, including sensitive settings like DHIS2 instance, username, and password. For automation, credentials and settings should be externalized rather than hardcoded in scripts.

### Tag the parameters cell

Since we are using [papermill](https://papermill.readthedocs.io/) to run the notebook, we first need to tell papermill where the parameters are defined. As described in the [papermill documentation](https://papermill.readthedocs.io/en/latest/usage-parameterize.html#designate-parameters-for-a-cell), this is done by adding a `parameters` tag to the notebook cell containing the parameters. 

### Create the parameters yaml file

Papermill can then [read parameters from a yaml file](https://papermill.readthedocs.io/en/latest/usage-execute.html#using-a-parameters-file), and then inject and override those defined in the notebook cell with the `parameters` tag. For this tutorial, we have included an [import-temperature-config.yaml](./example/configs/import-temperature-config.yaml) file where we set the parameters to import temperature data instead of the default precipitation. 

```bash
DHIS2_BASE_URL: https://play.im.dhis2.org/stable-2-42-3-1
DHIS2_USERNAME: admin
DHIS2_PASSWORD: district

DHIS2_DATA_ELEMENT_ID: urBVcn8nZ7V
DHIS2_TIMEZONE_OFFSET: 0
DHIS2_DRY_RUN: True

IMPORT_VARIABLE: 2m_temperature
IMPORT_VALUE_COL: t2m
IMPORT_IS_CUMULATIVE: False
IMPORT_FROM_UNITS: kelvin
IMPORT_TO_UNITS: degC

IMPORT_START_DATE: 2025-01

DOWNLOAD_FOLDER: /app/data
DOWNLOAD_PREFIX: era5_hourly_temperature
TEMPORAL_AGGREGATION: mean
```

This approach allows:

- **Security** - credentials stay out of version control
- **Flexibility** - different settings for different import schedules
- **Docker compatibility** - containers can load the parameters using local config files

## 3) Configure Docker and cron scheduling

For production use, we run imports automatically on a schedule using Docker and Cron schedules.

To make our notebook run on a schedule, we have defined three files:

- **Dockerfile**
- **cronfile**
- **docker-compose**

### 3.1) Dockerfile

Defining a `Dockerfile` image is needed to define the virtual operating system with needed tools such as `cron` to run schedules, the code and script files to import the data, and install the packages and environment needed to run them. We include an example [Dockerfile](./example/Dockerfile) that has what we will use for this tutorial. Its contents look like this:

```bash
# start with a Python 3.13 base image
FROM python:3.13-slim

# install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    git \
    tzdata \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# set and enter the workspace
WORKDIR /app

# install the DHIS2 Climate Tools environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

To keep the Docker image generic and reusable, the Dockerfile only copies what we need to install the Python environment, without baking any notebooks, scripts, or configuration into the image itself.

The notebooks, cron configuration, and parameter files are provided later by mounting the project directory into the container at runtime using Docker Compose.

### 3.2) cronfile

To define the scheduled imports, we have created an example [cronfile](./example/cronfile) which looks like this:

```bash
# Set your local timezone here
TZ=Europe/Oslo

# Force the shell to bash (standardizes behavior)
SHELL=/bin/bash

# Add the Python/Pip installation path
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# ====================================================
# Define one or more commands to be run at a schedule
# Format is: {CRONPATTERN} {COMMAND}
# The > /proc/1/fd/1 2>&1 at the end redirects the cron logs to Docker logs

# Run ERA5 import for temperature at 02:00
0 2 * * * papermill --cwd /app /app/notebooks/import-era5-daily.ipynb /app/data/import-temperature.output.ipynb -f /app/configs/import-temperature-config.yaml --log-output --no-progress-bar > /proc/1/fd/1 2>&1
```

What the above `cronfile` does:

1. Creates a crontab entry for running `import-era5-daily.ipynb` using the parameters from `import-temperature-config.yaml`.
2. Forwards output to Docker logs for monitoring.
3. Runs continuously, executing the import according to the specified schedule.

Cron expression examples:

| Expression | Description |
|------------|-------------|
| `0 6 * * *` | Daily at 6:00 AM |
| `0 1 * * *` | Daily at 1:00 AM |
| `0 0 * * 0` | Weekly on Sunday at midnight |
| `0 0 1 * *` | Monthly on the 1st |

Use [crontab.guru](https://crontab.guru/) to build expressions.

### 3.3) docker-compose file

We also need a docker compose file which will build the Docker image, link to our local `example` folder, and run the `crontab` command on the [cronfile](./example/cronfile). We include an example [docker-compose.yaml](./example/docker-compose.yaml) file that can be used for this tutorial. It should look like this:

```bash
services:
schedule:
    build: .
    image: climate-scheduler:latest     # Explicit image name
    container_name: climate-scheduler   # Explicit container name
    restart: unless-stopped             # Restarts in the case of a crash
    environment:
    - TZ=Europe/Oslo                  # Set your local timezone here
    volumes:
    - .:/app                          # Links current folder content to app folder
    - ./data:/app/data          # Links local data folder to container folder
    - ~/.cdsapirc:/root/.cdsapirc:ro  # Links local CDS API key to container root user folder
    command: >
    sh -c "
        dos2unix /app/cronfile &&
        crontab /app/cronfile &&
        cron &&
        tail -f /dev/null
    "
```

Things to note:

- The line `.:/app` is important and means that the `/app` folder Docker container will automatically be synced with the contents of the current folder (`.`). This way, any changes to the notebook, the parameters, and the cronfile scheduled runs, will not require you to `docker build` the Docker image again. 
- The same goes for the line `./data:/app/data` which means that the data downloads inside the Docker container will actually end up inside the local `data` folder to allow full inspectiong and avoid cluttering the Docker container. 
- The line `~/.cdsapirc:/root/.cdsapirc:ro` makes your local CDS API key accessible in the Docker container `root` user folder. If you later change the Docker user then you have to update this to the correct user folder. This line is only needed for this particular workflow, because we are accessing data from the Climate Data Store (CDS). Other workflows may require other forms of authentication. 
- The line with `docs2unix` makes sure the `cronfile` is saved with LF line endings which is a common gotcha for Windows users, otherwise Cron will complain. 

## 4) Build and run the scheduler with docker compose

The files contained in the `example` folder should be enough to test run the provided import schedule on your computer. 

The only thing you have to change is updating the `DATA_ELEMENT_ID` in the `configs/import-temperature-config.yaml` file. If you are running against the public DHIS2 server, you can use the [Prepare Metadata notebook](../../guides/import-data/prepare-metadata.ipynb) to create the needed data elements. 

Note that the included parameters file uses `DRY_RUN = True`, so remember to set this to `False` if you want to actually import into your instance. 

From the root of the DHIS2 Climate Tools repository, navigate to the scheduling `example` folder:

```bash
cd docs/workflows/scheduling/example
```

Starting the docker compose file will build the image (only the first time) and start the cron scheduler:

```bash
    docker compose up --detach --build
```

To check that the docker container started successfully and is running:

```bash
    docker ps
```

To verify that the docker container and cron schedule uses the correct timezone:

```bash
    docker exec climate-scheduler date
```

To check the last `n` timestamped logs:

```bash
    docker logs --timestamps -n 20 climate-scheduler
```

Now the ERA5-Land imports should repeat at regular intervals as specified in the `cronfile`, for as long as the docker container `climate-scheduler` is running. If something unexpected happens or it crashes, the container will restart and continue where it left off. 

### Making changes to the notebook, parameters, or schedules

If you make any changes to any of the files or schedules, you simply have to restart the docker container in order to restart `cron` and for the changes to take effect:

```bash
    docker compose down
    docker compose up --detach --build
```

## 5) Adding multiple scheduled jobs

You can also add multiple schedules to the same `cronfile`, so that one schedule runs the notebook with the temperature parameters file, and another schedule with a precipitation parameters file, and so on. 

Your `configs` folder would then have one config for temperature and another for precipitation:

```bash
    └── configs
        ├── import-temperature-config.yaml
        └── import-precipitation-config.yaml
```

And your `cronfile` would have two schedules instead of one:

```bash
    # Run ERA5 import for temperature at 02:00
    0 2 * * * papermill --cwd /app /app/notebooks/import-era5-daily.ipynb /app/data/import-temperature.output.ipynb -f /app/configs/import-temperature-config.yaml --log-output --no-progress-bar > /proc/1/fd/1 2>&1

    # Run ERA5 import for precipitation at 03:00
    0 3 * * * papermill --cwd /app /app/notebooks/import-era5-daily.ipynb /app/data/import-precipitation.output.ipynb -f /app/configs/import-precipitation-config.yaml --log-output --no-progress-bar > /proc/1/fd/1 2>&1
```

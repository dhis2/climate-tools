---
title: Open Climate Service
---

[Open Climate Service](https://dhis2.github.io/open-climate-service/) is an open-source platform that integrates climate and earth observation data from many sources and serves it — per country or region — through open standards (STAC, Zarr over HTTP, and the [openEO](https://openeo.org/) API).

Where the rest of DHIS2 Climate Tools downloads and processes data **client-side** in these notebooks, Open Climate Service does the heavy lifting **server-side**: a running instance ingests datasets (CHIRPS, ERA5-Land, WorldPop, and more), keeps them up to date, stores them as GeoZarr, and exposes reusable processing workflows. The notebooks in this section show how to talk to such an instance from Python with the lightweight `open-climate-service` client.

:::{note}
These notebooks require access to a **running Open Climate Service instance**. See the [Open Climate Service documentation](https://dhis2.github.io/open-climate-service/) to set one up, or use an instance provided by your team.
:::

## Install the client

The client is distributed on PyPI as `open-climate-service`. The base install only needs to talk to an instance over HTTP; the `[xarray]` extra adds support for opening published datasets as an `xarray.Dataset`:

```bash
pip install "open-climate-service[xarray]"
```

## Notebooks

- [Connect and explore](connect-and-explore.ipynb) — connect to an instance, discover datasets and workflows, and open a dataset as `xarray`.
- [Use with the openEO Python client](use-with-openeo-client.ipynb) — drive an instance with the standard, portable openEO client.
- [Aggregate to organisation units](aggregate-to-org-units.ipynb) — run a server-side workflow that aggregates a dataset to your org units, then import the result into DHIS2.
- [Prepare data for Chap](prepare-data-for-chap.ipynb) — produce a Chap-ready CSV from a single workflow call.
- [Animate with mapflow](animate-with-mapflow.ipynb) — turn a dataset into a time-lapse video.

## How it fits with Climate Tools

Open Climate Service and Climate Tools are complementary — you can use either or both:

| | Open Climate Service | Climate Tools |
|---|---|---|
| Runs | As a server, per country/region | In your notebooks |
| Role | Ingests, stores (GeoZarr), and processes data | Explores, analyses, and imports data |
| You reach it via | The `open-climate-service` client / openEO | `dhis2eo`, `xarray`, `geopandas`, … |

A common pattern is to let an Open Climate Service instance handle ingestion, storage and aggregation, and use Climate Tools notebooks to drive it, inspect the results, and import them into DHIS2 or Chap.

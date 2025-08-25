---
title: Exporting organization unit geometries
short_title: Export org unit geometries
---

To aggregate climate, weather and environmental data to organization units
we need to have the geometries (polygons or points). Org units geometries
can be downloaded in the DHIS2 Maps app, or through the DHIS2 Web API.

## DHIS2 Maps

Org units can easily be downloaded from DHIS2 Maps:

1. Open DHIS2 Maps
2. Add a new Org units layer
3. Select "Download data" under the "More actions" menu

The organization units will be downloaded as a GeoJSON file.

```{figure} images/maps-geojson-download-1.png
:alt: Sunset at the beach
:align: left
:width: 60%

Select __Maps__ from the app menu in the DHIS2 header bar.
```

```{figure} images/maps-geojson-download-2.png
:align: left

In DHIS2 Maps, click on __Add layer__ and __Org units__
```

```{figure} images/maps-geojson-download-3.png
:align: left
:width: 80%

Select the org units you would like to download, e.g. the district level.
Click on __Add layer__.
```

```{figure} images/maps-geojson-download-4.png
:align: left

Select __Download data__ under the __More actions__ menu and confirm
that you want to download the data. The org units are downloaded as GeoJSON
with the file name "organisation units.geojson". Rename the file if you want
to describe what it contains (e.g. "sierra-leone-districts.geojson").
```

## DHIS2 Web API

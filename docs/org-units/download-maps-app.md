---
title: Download org units from DHIS2 Maps
short_title: Download from DHIS2 Maps
---

Organisation units can easily be downloaded in GeoJSON format from DHIS2 Maps:

1. Open DHIS2 Maps
2. Add a new Org units layer
3. Select "Download data" under the "More actions" menu

The organisation units will be downloaded as a GeoJSON file.

```{figure} images/maps-geojson-download-1.png
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
<<<<<<< HEAD:docs/src/exporting-organization-units.md

## DHIS2 Web API

It is also possible to get org units geometries is via DHIS2 Web API. One can simply add ```.geojson``` extension to the ```<api/organisationUnits>``` endpoint. ```api/organsiationUnits.geojson``` endpoint accepts two parameters: ```level``` (default 1) and ```parent``` (default root). 

One can specify as many level and parent params as needed. It is therefore best to first decide for which level(s) and/or children of orgunit(s) we are interested to fetch the geometries. For example, if we are interested to fetch for the entire orgunits - i.e. all levels - we first need to know how many levels are available in the system. Orgunit level information is available from endpoint ```api/organisationUnitLevels.json?fields=id,name,level```. Below is a sample output from **Sierra Leone** database.
```json
{
  "organisationUnitLevels": [
    {
      "name": "Chiefdom",
      "level": 3,
      "id": "tTUf91fCytl"
    },
    {
      "name": "District",
      "level": 2,
      "id": "wjP19dkFeIk"
    },
    {
      "name": "Facility",
      "level": 4,
      "id": "m9lBJogzE95"
    },
    {
      "name": "National",
      "level": 1,
      "id": "H1KlN4QIauv"
    }
  ]
}
```

Once we have the level information, we can use that to fetch geometries. See a sample below.

**GET api call:** ```api/organisationUnits.geojson?level=1&level=2&level=3&level=4```

**sample output** (for brevity lots of coordinates are truncated from the second feature data)
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "plnHVbJR6p4",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -12.9487,
          9.0131
        ]
      },
      "properties": {
        "code": "OU_211234",
        "name": "Ahamadyya Mission Cl",
        "level": "4",
        "parent": "QywkxFudXrC",
        "parentGraph": "ImspTQPwCqd/PMa2VCrupOd/QywkxFudXrC",
        "groups": [
          "GGghZsfu7qV",
          "oRVt7g429ZO"
        ]
      }
    },
    {
      "type": "Feature",
      "id": "YuQRtpLP10I",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -11.3516,
              8.0819
            ],
            [
              -11.3553,
              8.0796
            ],
            ...
            ,
            [
              -11.3516,
              8.0819
            ]
          ]
        ]
      },
      "properties": {
        "code": "OU_539",
        "name": "Badjia",
        "level": "3",
        "parent": "O6uvpzGd5pu",
        "parentGraph": "ImspTQPwCqd/O6uvpzGd5pu",
        "groups": [
          "gzcv65VyaGq"
        ]
      }
    }
  ]
}
```
The output contains geometry information of all orgunits living on the mentioned levels. Two types of geometry information are returned - a point (with lat,lng) or a polygon (with several points of lat,lng forming the shape). As can be seen from the output, apart from the gemoetry information additional detailed properties - for example code, name, level, parent, parent graph and groups - about each orgunit are returned.

Result can be saved as a .geojson file and latter imported to a DHIS2 instance via Import/Export app 
```{figure} images/geometry-import-app.png
:align: left
```
=======
>>>>>>> main:docs/org-units/download-maps-app.md

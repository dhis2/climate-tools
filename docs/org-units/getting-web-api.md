---
title: Getting org units from DHIS2 Web API
short_title: Getting from Web API
---
This page shows practical ways to fetch organisation unit (OU) data from the DHIS2 Web API using `dhis2-python-client` library.

In the **climate-tools** environment, `dhis2-python-client` library is already installed. You only need to come up with your DHIS2 credintials and server address to use this library. Below is a basic usage:

```{code-cell} python
from dhis2_client import DHIS2Client
from dhis2_client.settings import ClientSettings

# Client configuration
cfg = ClientSettings(
  base_url="http://localhost:8080",
  username="admin",
  password="district")

client = DHIS2Client(settings=cfg)

info = client.get_system_info()
# Check if everything is working.
# You should see your current DHIS2 version info.
print(info["version"])
```

Once you are sure to be able to make connection with your DHIS2 instance, you can proceed to fetching orgunits. But first you need to decide which orgunit(s) to fetch. The library offers a couple of handy methods for this. Please see [here](https://github.com/dhis2/dhis2-python-client) for more usage examples of the library

### List OUs by level (auto‑paged)

```python
print("Fetching org units at level 3...")
# client.get_organisation_units() returns an iterable dict
for ou in client.get_organisation_units(level=3, fields="id,name", order="name:asc"):
    print(ou)
```

Given that you have org units at level 3, you should be able to see something like the following.

```console
Fetching org units at level 3...
{'name': 'Badjia', 'id': 'YuQRtpLP10I'}
{'name': 'Bagruwa', 'id': 'jPidqyo7cpF'}
{'name': 'Baoma', 'id': 'vWbkYPRmKyS'}
{'name': 'Bargbe', 'id': 'dGheVylzol6'}
{'name': 'Bargbo', 'id': 'zFDYIgyGmXG'}
{'name': 'Barri', 'id': 'RzKeCma9qb1'}
{'name': 'Bendu Cha', 'id': 'EB1zRKdYjdY'}
{'name': 'Biriwa', 'id': 'fwH9ipvXde9'}
{'name': 'BMC', 'id': 'ENHOJz3UH5L'}
{'name': 'Bombali Sebora', 'id': 'KKkLOTpMXGV'}
```

### Fetch all OUs in the system

```python
ous = list(client.get_organisation_units(level=3, fields="id,name", order="name:asc"))
print("Total number of ous available: ", len(ous))
```

`client.get_organisation_units()` returns an `Iterable` and can be converted to a `List` Dict for further processing. However, please be careful of memory usage if you have a huge number of org units in your system.

Running the above gives you something like the following:

```console
Total number of ous available:  1332
```

While `.get_organisation_units(...)`is a convenient method to faciliate page by page data fetching, the library also allows a raw access where you can pass filters and params direct to DHIS2 API. Below is an example

### Get a single OU by UID

```python
print("Fetching a specific org unit by ID...")
ou_id = "O6uvpzGd5pu"  # Change this to your desired org unit ID
org_unit = client.get("/api/organisationUnits/" + ou_id, params={"fields": "id,name,level,parent"})
print(org_unit) # Print the fetched org unit details
```

### Fetch multiple organisation units by IDs

```python

print("Fetching multiple org units by IDs...")
# Suppose you want these org unit IDs:
ou_ids = ["ImspTQPwCqd", "O6uvpzGd5pu"]

# Call the raw API with the `ids` as filter
resp = client.get(
    "/api/organisationUnits",
    params={
        "fields": "id,displayName,parent[id,displayName]",
        "filter": "id:in:[" + ",".join(ou_ids) + "]",
    },
)

# DHIS2 returns a JSON object with the "organisationUnits" array
for ou in resp["organisationUnits"]:
    print(ou["id"], ou["displayName"])
```

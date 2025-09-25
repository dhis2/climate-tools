# dhis2-python-client

## Introduction

The **DHIS2 Python Client** is a lightweight yet powerful library designed to connect DHIS2 with the wider data science ecosystem.

It was built to meet the needs of **data practitioners, analysts, and program managers** who rely on DHIS2 as a cornerstone of their information systems. While many climate, environmental, or socio-economic datasets may come from outside DHIS2, this client ensures that DHIS2 data can be **easily accessed, integrated, and contributed back**. Used alongside other climate-tools, it becomes part of a broader ecosystem that brings diverse data sources together for harmonization, orchestration, analysis, and ultimately decision making.

The client makes it simple to **pull** data out of DHIS2 for analysis and **push** curated results back into DHIS2 for use in dashboards, decision making, or further integration.

---

## Why This Library is Needed

Effective decision making in health, climate, and beyond depends on **timely, harmonized data** — whether linking malaria or dengue with rainfall, assessing facility readiness during heatwaves, or connecting air quality to NCDs. DHIS2 often provides the **program and health side**, but integrating it with external datasets can be complex.

Metadata management adds another hurdle: creating or updating data elements, datasets, or organisation units in the DHIS2 Maintenance app requires repetitive, manual steps. The DHIS2 Python Client addresses these challenges by providing a **clear, reliable interface** that:

- **Simplifies access** to DHIS2 by removing the complexity of API calls, authentication, and paging
- **Enables bi-directional exchange** (pulling and pushing data)
- **Delivers consistent outputs** ready for analysis and pipelines
- **Streamlines metadata creation** through scripted, reproducible updates

---

## Getting started

The library is available from the [DHIS2 Python Client GitHub repository](https://github.com/dhis2/dhis2-python-client).

It requires **Python 3.10+** and access to a DHIS2 server. Installation is currently from source:

```bash
git clone https://github.com/dhis2/dhis2-python-client.git
cd dhis2-python-client
pip install -e .
```

---

## Looking Ahead

The DHIS2 Python Client serves as a **bridge between DHIS2 and the wider data ecosystem**.

It makes it easier to **pull data from DHIS2** and **push results back in**, helping position DHIS2 as part of integrated information systems. On its own it improves access and efficiency; combined with other climate-tools, it supports the broader goal of **harmonizing diverse datasets into useful evidence** for better programs and more resilient policies.

# Releasing New Versions of the DHIS2 Climate Tools Guidebook

This repository contains an educational website implemented primarily as
Jupyter notebooks. Releases are intended to provide **reproducible snapshots**
of both the content and the execution environment.

This document describes how maintainers create new releases and how versions
are communicated to users:

1. Update requirements.txt

    Dependencies are specified in `requirements.txt` and should be updated to the latest required dependency versions if there have been any changes. 

2. Update the recommended Python version

    Update the `python-version.txt` file to the latest tested Python version. For example:

        3.10

3. Create a new GitHub Release in the browser. 

    Give it a version tag in the format `v<year>.<1+>`, incrementing by one for each new version in a given year.

    Examples:
    - `v2026.1`
    - `v2026.2`

4. When a new GitHub version tag is detected, the website will automatically deploy and update the official website at [climate-tools.dhis2.org](climate-tools.dhis2.org). 

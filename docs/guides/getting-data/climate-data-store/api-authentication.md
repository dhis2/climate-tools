# API Authentication

In order to download data programmatically from ECMWF's Climate Data Portal (CDS), you need to first complete the steps below. 

### 1. Create an ECMWF User

The first step is to [create an ECMWF user](https://www.ecmwf.int/user/login).

### 2. Create a user credentials file

Next, you need to create a file on your computer containing your user credentials:

- Go to the [CDSAPI Setup page](https://cds.climate.copernicus.eu/how-to-api) and make sure to login. 
- Once logged in, scroll down to the section "Setup the CDS API personal access token". 
  - This should show your login credentials, and look something like this:

        url: https://cds.climate.copernicus.eu/api
        key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

- Copy those two lines to a file `.cdsapirc` in your user's $HOME directory.

### 3. Accept the dataset license

Lastly, ECMWF requires that you manually accept the user license for each dataset that you download. 

- Visit the Download page of the dataset you want to download.
- Scroll down until you get to the "Terms of Use" section.
- Click the button to accept and login with your user if you haven't already.
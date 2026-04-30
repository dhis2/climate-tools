# API Authentication

In order to download data programmatically from the Destination Earth - Earth Data Hub, you need to first complete the steps below. 

### 1. Create a Destination Earth account

The first step is to [create a Destination Earth (DestinE) user account](https://earthdatahub.destine.eu/).

### 2. Create a user credentials file

Next, you need to create a file on your computer containing your user credentials:

- Create a file `.netrc` (Unix) or `_netrc` (Windows) in your user's $HOME directory, which should look like this:

      machine data.earthdatahub.destine.eu
          password <your personal access token>

- To get your personal access token:
  - Login and go to your [Earth Data Hub account page](https://earthdatahub.destine.eu/account-settings). 
  - Scroll down to the section "My personal access tokens". 
  - View or copy your default access token, or create a new one. 

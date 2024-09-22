[<img src="https://github.com/uberfastman/yfpy/raw/main/docs/_static/yfpy-logo.svg" width="400"/>](https://github.com/uberfastman/yfpy)

## YFPY - Yahoo Fantasy Sports API Wrapper
Python API wrapper for the Yahoo Fantasy Sports public API

*Author: Wren J. R. (uberfastman)*

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/uberfastman/yfpy?color=yellowgreen&label=latest%20release&sort=semver)](https://github.com/uberfastman/yfpy/releases/latest)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/uberfastman/yfpy?color=yellowgreen&label=latest%20version&sort=semver)](https://github.com/uberfastman/yfpy/tags)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/uberfastman/yfpy/python-package.yml?color=brightgreen&label=build)](https://github.com/uberfastman/yfpy/actions/workflows/python-package.yml)

[![PyPI](https://img.shields.io/pypi/v/yfpy.svg?style=flat)](https://pypi.python.org/pypi/yfpy)
[![PyPI](https://img.shields.io/pypi/dm/yfpy.svg?style=flat)](https://pypi.python.org/pypi/yfpy)
[![PyPI](https://img.shields.io/pypi/pyversions/yfpy.svg?style=flat)](https://pypi.python.org/pypi/yfpy)
[![PyPI](https://img.shields.io/pypi/l/yfpy.svg?style=flat)](https://pypi.python.org/pypi/yfpy)

---

<sub>***Do you like the YFPY API wrapper? Star the repository on GitHub and please consider helping support its ongoing development:***</sub>

[<img src="https://github.com/uberfastman/yfpy/raw/main/resources/images/donate-paypal.png" width="75"/>](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=VZZCNLRHH9BQS) [<img src="https://github.com/uberfastman/yfpy/raw/main/resources/images/donate-bitcoin.png" width="75"/>](https://share.trustwallet.com/ZoAkTpY1I9) [<img src="https://github.com/uberfastman/yfpy/raw/main/resources/images/donate-ethereum.png" width="75"/>](https://share.trustwallet.com/MF8YBO01I9)

|                                                                <sub><sup>Cryptocurrency</sup></sub> |                                                      <sub><sup>Address</sup></sub>                                                       |
|----------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                 <sub><sup>Bitcoin (BTC)</sup></sub> |                                    <sub><sup>`bc1qataspvklhewtswm357m0677q4raag5new2xt3e`</sup></sub>                                    | 
|                                                                <sub><sup>Ethereum (ETH)</sup></sub> |                                    <sub><sup>`0x5eAa522e66a90577D49e9E72f253EC952CDB4059`</sup></sub>                                    |

<sub><sup></sup></sub>

---

**[READ THE DOCS HERE!](https://yfpy.uberfastman.com)**
<br/>
<sup>Detailed documentation on YFPY can be found at [https://yfpy.uberfastman.com](https://yfpy.uberfastman.com).</sup>

### Table of Contents
* [About](#about)
* [Installation](#installation)
    * [Pip](#pip)
    * [Manual](#manual)
* [Setup](#setup)
    * [Yahoo Developer Network App](#yahoo-developer-network-app)
    * [Environment Variables](#environment-variables)
* [Usage](#usage)
    * [Authentication](#authentication)
        * [Programmatic Persistent Authentication](#programmatic-persistent-authentication)
        * [Persistent Authentication Using Access Token Fields](#persistent-authentication-using-access-token-fields)
        * [Persistent Authentication Using Access Token JSON](#persistent-authentication-using-access-token-json)
    * [Querying the Yahoo Fantasy Sports API](#querying-the-yahoo-fantasy-sports-api)
    * [Docker](#docker)
        * [Docker Development](#docker-development)
        * [Docker Image Deployment](#docker-image-deployment)
* [Testing](#testing)
    * [Unit Tests](#unit-tests)
    * [Integration Tests](#integration-tests)
    * [Run Tests](#run-tests)
* [Dependencies](#dependencies)
    * [Platform](#platform)
    * [Python](#python)
    * [Development](#development)
* [Troubleshooting](#troubleshooting)
    * [Yahoo Fantasy Sports API](#yahoo-fantasy-sports-api)

---

<a name="about"></a>
### About

YFPY is a comprehensive wrapper around the Yahoo Fantasy Sports API. It allows for easy retrieval and parsing of almost any data you might wish to extract and use from any Yahoo fantasy league to which your Yahoo account has access (or for public leagues). The primary focus of this wrapper is on fantasy football (NFL), but it also supports usage with fantasy hockey (NHL), fantasy baseball (MLB), and fantasy basketball (NBA). 

---

<a name="installation"></a>
### Installation

<a name="pip"></a>
#### Pip

* If you wish to use YFPY within another project, from within your project directory, run
    ```shell
    pip install yfpy
    ```
    
    or add `yfpy` to your project `requirements.txt`.

<a name="manual"></a>
#### Manual

* If you wish to download and use YFPY locally, clone the git repository:
  ```shell
  git clone git@github.com:uberfastman/yfpy.git
  ```

---

<a name="setup"></a>
### Setup

<a name="yahoo-developer-network-app"></a>
#### Yahoo Developer Network App

In order to use YFPY with private fantasy leagues, you must set up an app on your Yahoo account to allow access. Follow the step-by-step guide below for instructions on how to do so, or see [Getting Started](https://developer.yahoo.com/oauth2/guide/openid_connect/getting_started.html) in the Yahoo Developer Network docs for more details.

**Note:** *If you are only planning on using YFPY to pull "read only" data from public leagues, you do not need to do this.*

* Log in to a Yahoo account with access to whatever fantasy leagues from which you wish to retrieve data.
* Go to [https://developer.yahoo.com/apps/create/](https://developer.yahoo.com/apps/create/) and create an app (you must be logged into your Yahoo account as stated above). For the app, select the following options:
    * `Application Name` (**Required**): `yfpy` (you can name your app whatever you want, but this is just an example).
    * `Application Type` (**Required**): select the `Installed Application` radio button.
    * `Description` (*Optional*): you *may* write a short description of what the app does.
    * `Home Page URL` (*Optional*): if you have a web address related to your app you *may* add it here.
    * `Redirect URI(s)` (**Required**): this field must contain a valid redirect address, so you can use `https://localhost:8080`
    * `API Permissions` (**Required**): check the `Fantasy Sports` checkbox. You can leave the `Read` option selected (appears in an accordion expansion underneath the `Fantasy Sports` checkbox once you select it).
    * Click the `Create App` button.
    * Once the app is created, it should redirect you to a page for your app, which will show both a `Client ID` and a `Client Secret`.
    * Copy the `Client ID` and `Client Secret` and proceed with the steps in [Environment Variables](#environment-variables) or [Programmatic Persistent Authentication](#programmatic-persistent-authentication).

<a name="environment-variables"></a>
#### Environment Variables

YFPY now supports the usage of environment variables, either directly within the command line or using a `.env` file.

* Set up your `.env` file by making a copy of `.env.template` in the root project directory and renaming it `.env` (you can do this in the command line by running `cp .env.template .env`).
* Paste the `Client ID` and `Client Secret` retrieved by following the steps in [Yahoo Developer Network App](#yahoo-developer-network-app) into their respective environment variables in your `.env` file:
```dotenv
YAHOO_CONSUMER_KEY=<YAHOO_DEVELOPER_APP_CONSUMER_KEY_STRING>
YAHOO_CONSUMER_SECRET=<YAHOO_DEVELOPER_APP_CONSUMER_SECRET_STRING>
```
* YFPY is configured by default to check for environment variables for authentication with Yahoo, so you will now be able to proceed directly to [Authentication](#authentication).

**Note**: *You can disable the fallback to environment variables behavior during instantiation of a YFPY query by passing the argument `env_var_fallback=False` to the object:
```python
from yfpy.query import YahooFantasySportsQuery

query = YahooFantasySportsQuery(
    league_id="<YAHOO_LEAGUE_ID>",
    game_code="nfl",
    game_id=449,
    yahoo_consumer_key="<YAHOO_CONSUMER_KEY>",
    yahoo_consumer_secret="<YAHOO_CONSUMER_SECRET>",
    env_var_fallback=False
)
```

---

<a name="usage"></a>
### Usage

<a name="authentication"></a>
#### Authentication

* Follow the instructions in the [Installation](#installation) and [Setup](#setup) sections.
* The ***first*** time you use YFPY, a browser window will open up asking you to allow your app to access your Yahoo fantasy sports data. You ***MUST*** hit allow, and then copy the verification code that pops up into the command line prompt where it will now be asking for verification, hit enter, and the OAuth2 three-legged handshake should be complete and your data should have been successfully retrieved.

**Note**: *If you are running YFPY in Docker, instead of opening a new browser window, YFPY will output a URL to the command line, which you must then copy to a browser window in order to log in to your Yahoo account, allow access to your app, and retrieve the required verification code.*

<a name="programmatic-persistent-authentication"></a>
##### Programmatic Persistent Authentication

YFPY supports programmatic authentication using `yahoo_consumer_key` and `yahoo_consumer_secret` arguments when instantiating a `YahooFantasySportsQuery` object. Additionally, you can pass in either a valid JSON string or a Python dictionary to `yahoo_access_token_json` containing all required fields of a Yahoo access token.

* Providing `yahoo_consumer_key` and `yahoo_consumer_secret` overrides any values provided in a `.env` file.
* Providing a value to `yahoo_access_token_json` overrides both `yahoo_consumer_key`/`yahoo_consumer_secret` values *and* any values provided in a `.env` file for a Yahoo access token.
  * Required fields (either in a JSON string with escaped double quotes or a Python dictionary) for the value of `yahoo_access_token_json` are the following:
    * `access_token`
    * `consumer_key`
    * `consumer_secret`
    * `guid`
    * `refresh_token`
    * `token_time`
    * `token_type`
  * The `consumer_key` and `consumer_secret` fields in `yahoo_access_token_json` override 

Example of Using `yahoo_access_token_json`:
```python
from yfpy.query import YahooFantasySportsQuery

query = YahooFantasySportsQuery(
    league_id="<YAHOO_LEAGUE_ID>",
    game_code="nfl",
    game_id=449,
    yahoo_access_token_json={
        "access_token": "<YAHOO_ACCESS_TOKEN>",
        "consumer_key": "<YAHOO_CONSUMER_KEY>",
        "consumer_secret": "<YAHOO_CONSUMER_SECRET>",
        "guid": "<YAHOO_TOKEN_GUID>",
        "refresh_token": "<YAHOO_REFRESH_TOKEN>",
        "token_time": 1234567890.123456,
        "token_type": "bearer"
    }
)
```

<a name="persistent-authentication-using-access-token-fields"></a>
##### Persistent Authentication Using Access Token Fields

* YFPY no longer uses JSON files to store Yahoo credentials or access tokens. However, if you wish to preserve your access token in order to remain verified, you can now instantiate a YFPY query with `save_token_data_to_env_file=True`, which will write all required Yahoo access token fields to an `.env` file (the `.env` file will be located in the project root directory by default, but you can tell YFPY to use a different `.env` file by specifying the path to a custom location using `env_file_location`). 
* For all subsequent runs of your app, you should be able to keep retrieving Yahoo fantasy sports data using YFPY without re-verifying, since the generated refresh token should now just renew whenever you use the same `.env` file to authenticate your app.

<a name="persistent-authentication-using-access-token-json"></a>
##### Persistent Authentication Using Access Token JSON

* YFPY *also* supports the use of a **single** environment variable by providing a valid JSON string in `YAHOO_ACCESS_TOKEN_JSON`. This environment variable is only used if `env_var_fallback=True` when instantiating a YFPY query.

<a name="querying-the-yahoo-fantasy-sports-api"></a>
#### Querying the Yahoo Fantasy Sports API

* See the documentation on the  [`yfpy.query.YahooFantasySportsQuery`](https://yfpy.uberfastman.com/_autosummary/yfpy.query.YahooFantasySportsQuery.html#yfpy.query.YahooFantasySportsQuery) class for example usage of all available queries.
* See [`quickstart/quickstart.py`](https://github.com/uberfastman/yfpy/blob/main/quickstart/quickstart.py) for example usage output.
  * Uncomment/comment out whichever configuration values in their respective functions with which you wish to experiment.
  * Uncomment/comment out whichever query lines in the `RUN QUERIES` section you wish to run.
  * Uncomment/comment out whichever query lines in the `CHECK FOR MISSING DATA FIELDS` section you wish to check for any new/missing data fields returned by the Yahoo Sports Fantasy Football API.

<a name="docker"></a>
#### Docker

YFPY can be used within Docker for a more seamless, platform-agnostic experience.

* Run the Docker container (pulls the YFPY Docker image from GitHub Package Registry):
    ```shell
    docker compose up
    ``` 
* You can then run commands in the Docker container in two different ways:
  * Connect to the running container and run commands from within it:
    ```shell
    docker exec -it yfpy-package-1 bash
    ```
    Then:
    ```shell
    python quickstart/quickstart.py
    ```
  * Send commands to the running container from your host machine:
    ```shell
    docker exec -i yfpy-package-1 bash -c "python quickstart/quickstart.py"
    ```

<a name="docker-development"></a>
##### Docker Development

* Run the Docker container for local development (mount all local code into container):
    ```shell
    docker compose -f compose.yaml -f compose.dev.yaml up
    ```

<a name="docker-image-deployment"></a>
##### Docker Image Deployment

See [DEPLOYMENT.md](https://github.com/uberfastman/yfpy/blob/main/DEPLOYMENT.md) for Docker image deployment.

---

<a name="testing"></a>
### Testing

YFPY has a collection of fully functional code snippets that can be run using [pytest](https://docs.pytest.org/en/6.2.x/). These snippets demonstrate how to use YFPY to retrieve your Yahoo Fantasy Sports data.

<a name="unit-tests"></a>
#### Unit Tests

* See the [`test/unit`](https://github.com/uberfastman/yfpy/blob/main/test/unit/) directory for example code snippets using pytest.

<a name="integration-tests"></a>
#### Integration Tests

* See the [`test/integration`](https://github.com/uberfastman/yfpy/blob/main/test/integration/) directory for example code snippets using pytest.
* Before running any integration tests, make a copy of [`auth/.env.template`](https://github.com/uberfastman/yfpy/blob/main/auth/.env.template) in the [`auth/`](https://github.com/uberfastman/yfpy/blob/main/auth/) directory and rename it to `.env`.
* Copy your Yahoo `Client ID` and `Client Secret` into the environment variables in `.env` so that pytest can use them when hitting the Yahoo Fantasy Sports API.
* If this is the first time running pytest with your Yahoo API credentials, you ***MUST*** allow interactive prompts within pytest by using the `-s` flag.
* The fixture values in [`test/integration/conftest.py`](https://github.com/uberfastman/yfpy/blob/main/test/integration/conftest.py) are defined in [`quickstart/quickstart.py`](https://github.com/uberfastman/yfpy/blob/main/quickstart/quickstart.py), and can be changed for testing by uncommenting/commenting out the values inside each respective function.

<a name="run-tests"></a>
#### Run Tests

* You can invoke all pytest tests (both integration test and unit tests) by running the below from the root directory:
  * `pytest -v -s`
* If you want to run only the unit tests, you can run:
  * `pytest -v -s -m unit`
* If you want to run only the integration tests, you can run:
  * `pytest -v -s -m integration`

---

<a name="dependencies"></a>
### Dependencies

<a name="platform"></a>
#### Platform

YFPY has only been tested extensively on macOS, but is written to be platform-agnostic, and seems to work without issue on Windows and Linux. 

<a name="python"></a>
#### Python

YFPY requires Python 3.8 or later, and has been tested through Python 3.12.

<a name="development"></a>
#### Development

Direct project dependencies can be viewed in `requirements.txt`, and additional development and build dependencies (*not* including transitive dependencies) can be viewed in `requirements-dev.txt`.

---

<a name="troubleshooting"></a>
### Troubleshooting

<a name="yahoo-fantasy-sports-api"></a>
#### Yahoo Fantasy Sports API

Occasionally when you use the Yahoo Fantasy Sports API, there are hangups on the other end that can cause data not to transmit, and you might encounter an error similar to this:
```shell
Traceback (most recent call last):
  File "yfpy-app.py", line 114, in <module>
    var = app.run()
  File "/Users/your_username/PATH/T0/LOCAL/PROJECT/yfpy-app.py", line 429, in run
    for team in team_standings:
IndexError: list index out of range
```

Typically, when the above error (or a similar error) occurs, it simply means that one of the Yahoo Fantasy Sports API calls failed and so no data was retrieved. This can be fixed by simply re-running data query.

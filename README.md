[<img src="https://github.com/uberfastman/yfpy/raw/main/docs/_static/yfpy-logo.svg" width="400"/>](https://github.com/uberfastman/yfpy)

## YFPY - Yahoo Fantasy Sports API Wrapper
Python API wrapper for the Yahoo Fantasy Sports public API

*Author: Wren J. R. (uberfastman)*

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/uberfastman/yfpy?color=yellowgreen&label=latest%20release&sort=semver)](https://github.com/uberfastman/yfpy/releases/latest)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/uberfastman/yfpy?color=yellowgreen&label=latest%20version&sort=semver)](https://github.com/uberfastman/yfpy/tags)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/uberfastman/yfpy/CI%20Build/main?color=brightgreen&label=build)](https://github.com/uberfastman/yfpy/actions/workflows/python-package.yml)

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
* [Setup](#setup)
* [Usage](#usage)
* [Testing](#testing)
* [Dependencies](#dependencies)
* [Troubleshooting](#troubleshooting)

---

<a name="about"></a>
### About

YFPY is a comprehensive wrapper around the Yahoo Fantasy Sports API. It allows for easy retrieval and parsing of almost any data you might wish to extract and use from any Yahoo fantasy league to which your Yahoo account has access (or for public leagues). The primary focus of this wrapper is on fantasy football (NFL), but it also supports usage with fantasy hockey (NHL), fantasy baseball (MLB), and fantasy basketball (NBA). 

---

<a name="installation"></a>
### Installation

#### Pip

* If you wish to use YFPY within another project, from within your project directory, run
    ```shell
    pip install yfpy
    ```
    
    or add `yfpy` to your project `requirements.txt`.

#### Manual

* If you wish to download and use YFPY locally, clone the git repository:
  ```shell
  git clone git@github.com:uberfastman/yfpy.git
  ```

---

<a name="setup"></a>
### Setup

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
    * Make a copy of [`test/integration/EXAMPLE.private.json`](https://github.com/uberfastman/yfpy/blob/main/test/integration/EXAMPLE.private.json), rename it to just `private.json`, and copy the `Client ID` and `Client Secret` values to their respective fields (make sure the strings are wrapped regular quotes (`""`), NOT formatted quotes (`“”`)). The path to this file will be needed to point YFPY to your credentials.
    * Now you should be ready to initialize the OAuth2 connection between YFPY your Yahoo account.

---

<a name="usage"></a>
### Usage

#### Authentication

* Follow the instructions in the [Installation](#installation) and [Setup](#setup) sections.
* The ***first*** time you use YFPY, a browser window will open up asking you to allow your app to access your Yahoo fantasy sports data. You ***MUST*** hit allow, and then copy the verification code that pops up into the command line prompt where it will now be asking for verification, hit enter, and the OAuth2 three-legged handshake should be complete and your data should have been successfully retrieved.
* YFPY should have now generated a `token.json` for you in the same directory where you stored your `private.json` credentials, and for all subsequent runs of your app, you should be able to keep retrieving Yahoo fantasy sports data using YFPY without re-verifying, since the generated refresh token should now just renew whenever you use the same `token.json` file to authenticate your app.

#### Querying the Yahoo Fantasy Sports API

* See the documentation on the  [`yfpy.query.YahooFantasySportsQuery`](https://yfpy.uberfastman.com/_autosummary/yfpy.query.YahooFantasySportsQuery.html#yfpy.query.YahooFantasySportsQuery) class for example usage of all available queries.

---

<a name="testing"></a>
### Testing

YFPY has a collection of fully functional code snippets that can be run using [pytest](https://docs.pytest.org/en/6.2.x/). These snippets demonstrate how to use YFPY to retrieve your Yahoo Fantasy Sports data.

#### Unit

* See the [`test/unit`](https://github.com/uberfastman/yfpy/blob/main/test/unit/) directory for example code snippets using pytest.

#### Integration

* See the [`test/integration`](https://github.com/uberfastman/yfpy/blob/main/test/integration/) directory for example code snippets using pytest.
* Before running any integration tests, make a copy of [`test/integration/EXAMPLE.env`](https://github.com/uberfastman/yfpy/blob/main/test/integration/EXAMPLE.env) in the [`test/integration`](https://github.com/uberfastman/yfpy/blob/main/test/integration/) directory and rename it to `.env`.
* Copy your Yahoo `Client ID` and `Client Secret` into the environment variables in `.env` so that pytest can use them when hitting the Yahoo Fantasy Sports API.
* If this is the first time running pytest with your Yahoo API credentials, you ***MUST*** allow interactive prompts within pytest by using the `-s` flag.

#### Running

* You can invoke all pytest tests (both integration test and unit tests) by running the below from the root directory:
  * `pytest -v -s`
* If you want to run only the unit tests, you can run:
  * `pytest -v -s -m unit`
* If you want to run only the integration tests, you can run:
  * `pytest -v -s -m integration`

---

<a name="dependencies"></a>
### Dependencies

#### Platform

YFPY has only been tested extensively on macOS, but is written to be platform-agnostic, and seems to work without issue on Windows and Linux. 

#### Python

YFPY requires Python 3.7 or later, and has been tested through Python 3.10.

#### Development

Direct project dependencies can be viewed in `requirements.txt`, and additional development and build dependencies (*not* including transitive dependencies) can be viewed in `requirements-dev.txt`.

---

<a name="troubleshooting"></a>
### Troubleshooting

#### Yahoo Fantasy Sports API

Occasionally when you use the Yahoo Fantasy Sports API, there are hangups on the other end that can cause data not to transmit, and you might encounter an error similar to this:
```
Traceback (most recent call last):
  File "yfpy-app.py", line 114, in <module>
    var = app.run()
  File "/Users/your_username/PATH/T0/LOCAL/PROJECT/yfpy-app.py", line 429, in run
    for team in team_standings:
IndexError: list index out of range
```

Typically, when the above error (or a similar error) occurs, it simply means that one of the Yahoo Fantasy Sports API calls failed and so no data was retrieved. This can be fixed by simply re-running data query.

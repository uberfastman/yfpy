```
 __     ________ _______     __
 \ \   / /  ____|  __ \ \   / /
  \ \_/ /| |__  | |__) \ \_/ / 
   \   / |  __| |  ___/ \   /  
    | |  | |    | |      | |   
    |_|  |_|    |_|      |_|   
```

### Python API wrapper for the Yahoo Fantasy Sports public API
##### By Wren J. R. (uberfastman)

---

## Yahoo Fantasy Sports API Wrapper (YFPY)

### Table of Contents
* [About](#about)
* [Usage](#usage)
* [Setup](#setup)
* [Dependencies](#dependencies)
* [Troubleshooting](#troubleshooting)

---

<a name="about"></a>
### About

YFPY is a comprehensive wrapper around the Yahoo Fantasy Sports API. It allows for easy retrieval and parsing of almost any data you might wish to extract and use from any Yahoo fantasy league to which your Yahoo account has access (or for public leagues). The primary focus of this wrapper is on fantasy football (NFL), but it also supports usage with fantasy hockey (NHL), fantasy baseball (MLB), and fantasy basketball (NBA).
   
---

<a name="usage"></a>
### Usage

* In your project directory, run

    ```
    pip install yfpy
    ```
    
    or add `yfpy` to your project `requirements.txt`.
* Follow the instructions in the below [Setup](#setup) section.
* See `test/test.py` for fully functional code snippets within the query tests that demonstrate how to use YFPY.
* PLEASE NOTE: Assuming you followed the setup instructions correctly, the ***first*** time you use YFPY, a browser window will open up asking you to allow your app to access your Yahoo fantasy sports data. You ***MUST*** hit allow, and then copy the verification code that pops up into the command line prompt where it will now be asking for verification, hit enter, and the OAuth2 three-legged handshake should be complete and your data should have been successfully retrieved.
* YFPY should have now generated a `token.json` for you in the same directory where you stored your `private.json` credentials, and for all subsequent runs of your app, you should be able to keep retrieving Yahoo fantasy sports data using YFPY without re-verifying, since the generated refresh token should now just renew whenever you use the same `token.json` file to authenticate your app.

---

<a name="setup"></a>
### Setup

* Log in to a Yahoo account with access to whatever fantasy leagues from which you wish to retrieve data.
* Go to [https://developer.yahoo.com/apps/create/](https://developer.yahoo.com/apps/create/) and create an app (you must be logged into your Yahoo account as stated above). For the app, select the following options:
    * `Application Name` (**Required**): `yfpy` (you can name your app whatever you want, but this is just an example).
    * `Application Type` (**Required**): select the `Installed Application` radio button.
    * `Description` (*Optional*): you *may* write a short description of what the app does.
    * `Home Page URL` (*Optional*): if you have a web address related to your app you *may* add it here.
    * `Redirect URI(s)` (**Required**): this field must contain a valid redirect address, so you can use `localhost:8080`
    * `API Permissions` (**Required**): check the `Fantasy Sports` checkbox. You can leave the `Read` option selected (appears in an accordion expansion underneath the `Fantasy Sports` checkbox once you select it).
    * Click the `Create App` button.
    * Once the app is created, it should redirect you to a page for your app, which will show both a `Client ID` and a `Client Secret`.
    * Make a copy of `examples/EXAMPLE-private.json`, rename it to just `private.json`, and copy the `Client ID` and `Client Secret` values to their respective fields (make sure the strings are wrapped regular quotes (`""`), NOT formatted quotes (`“”`)). The path to this file will be needed to point YFPY to your credentials.
    * Now you should be ready to initialize the OAuth2 connection between YFPY your Yahoo account.

---

<a name="dependencies"></a>
### Dependencies

YFPY has only been tested on macOS, but is written to be platform agnostic. It runs only in Python 3, and has only been tested with Python 3.7.

Direct project dependencies can be viewed in `requirements.txt`, and all dependencies, including transitive dependencies, can be viewed in `dev-requirements.txt`.

---

<a name="troubleshooting"></a>
### Troubleshooting

Occasionally when you use the Yahoo fantasy sports API, there are hangups on the other end that can cause data not to transmit, and you might encounter an error similar to this:
```
Traceback (most recent call last):
  File "yfpy-app.py", line 114, in <module>
    var = app.run()
  File "/Users/your_username/PATH/T0/LOCAL/PROJECT/yfpy-app.py", line 429, in run
    for team in team_standings:
IndexError: list index out of range
```

Typically when the above error (or a similar error) occurs, it simply means that one of the Yahoo Fantasy Sports API calls failed and so no data was retrieved. This can be fixed by simply re-running data query.

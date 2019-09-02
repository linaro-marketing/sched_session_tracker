# sched_session_tracker
This repo hosts a python3 script to create, update and delete entries in a Google sheet based on a sched.com event export. This will be used by external AV contractors that need to track which sessions have been recorded/edited at the event.

## Usage

### Step 1 - Clone this repo

Open up a new terminal and clone this repo:

If you have SSH setup with git:

```bash
$ git clone git@github.com:linaro-marketing/sched_session_tracker.git && cd sched_session_tracker
....
```

Otherwise use https:

```bash
$ git clone https://github.com/linaro-marketing/sched_session_tracker.git && cd sched_session_tracker
....
```

### Step 2 - Setup your Python environment (virtualenv)

The best way to manage a python script/project is to use a virtualevn/pipenv. This ensures that all modules required by the project are isolated on a per-project basis and not installed via your global python installation (which tend's to be a bad idea...).

See if you have virtualenv installed:

```bash
$ virtualenv --version
15.1.0
```

Create a new python3 virtualenv for this project:

```bash
$ virtualenv -p python3 venv
creating virtualenv....
```

Once created you'll need to source the venv in your current terminal by using `. venv/bin/activate` or `source venv/bin/activate`

```bash
$ source venv/bin/activate
...
```

Now, whenever you run python3, your virtualenv will be used keeping your global python installation clean! Finish by installing the modules required by this projects scripts:


```bash
$ pip3 install -r requirements.txt
Installing....
```

********

If you don't have virtualenv then get it! If you already have pip3 then just run:

```bash
$ sudo pip3 install virtualenv
...
```

Read the docs:
- [https://virtualenv.pypa.io/en/latest/](https://virtualenv.pypa.io/en/latest/)
- [Install virtualenv on Ubuntu 18.04](https://gist.github.com/frfahim/73c0fad6350332cef7a653bcd762f08d)
- [Install virtualenv on MacOS](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)
- [Install virtualenv on Windows](https://thinkdiff.net/python/how-to-install-python-virtualenv-in-windows/)

### Step 2 - Create a Google Cloud Client Application

This project uses Google's Sheet python API.

Head over to [Google's Cloud Service](https://console.cloud.google.com/apis/credentials) and click `Create Credentials -> OAuth Client ID`. Make sure to select `other` for the application type otherwise you will not be able to validate and fetch your generated OAuth token.

Once you've done this you'll see your ID appear in the `OAuth 2.0 Client ID's` section on the same page. Then click the download icon to download your client_secret******.json file and save into the root of the `sched_session_tracker` directory which you just cloned.

### Step 3 - Get your token from Google!

So you've setup your client application in the Google Cloud Console and now you need to retreive your token.

### Step 4...


The `SchedSessionTracker` class requires the following arguments:

## Class positional args

| Arg | Description |
| --- | ----------- |
| Sched Event URL | Takes the url to your sched event e.g. https://linaroconnectsandiego.sched.com. Used when making API calls.|
| API Key file | This argument takes the name of a secret file to be used when pulling in the sched.com api key.
Defautls to API_KEY.secret (so add your API Key to this file)

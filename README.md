LiveEnsure demo application
============================

Two apps are included in this django app
- Social Chat application
- Healthcare application

### Step to setup

- Download or clone this repo
- Update `settings.py` INSTALLED_APPS to add `demosocial` app

```
INSTALLED_APPS = [
    ...
    'demosocial'
]
```
- Add keys to settings file to access liveensure API

```
LIVE_ENSURE = {
    "API_KEY": "<API key>",
    "API_PASSWORD": "<API password>",
    "AGENT_ID": "<Agent id>",
    "API_HOST": "<API host>",
    "GOOGLE_MAP_KEY": "<Google Map Key(optional, but map will work without this)>"
}
```

- Update urls.py to add urls for demosocial app

```
from django.conf.urls import include
...
urlpatterns = [
    ...
    url(r'^demo/', include('demosocial.urls')),
]
```

### Running the application

Urls for this applications are

- For Admin page: `/demo/admin`
- For Social chat application `/demo/social`
- For Healthcare demo: `demo/healthcare`

Step to see the demo

- First go to admin page and set parameters for challenge.
- Then go to any app and login.


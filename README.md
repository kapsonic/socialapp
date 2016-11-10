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

- Update urls.py to add urls for demosocial app

```
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


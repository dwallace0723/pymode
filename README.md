## PyMode

PyMode is a Python library to enable typed interactions with the [Mode Analytics API](http://developer.modeanalytics.com/).

### Installation

```
pip install pymode
```

### Usage

```
import pymode

# First create a Mode instance:

# Explicitly setting api token and api password
m = Mode('<your-org-name>','you-mode-api-token','your-mode-api-password')

# api token and api password set as environment variables
m = Mode('<your-org-name>')

for space in m.get_spaces():
    r = space.get_reports()
    print r.name
```

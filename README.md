## PyMode

PyMode is a Python library to enable typed interactions with the [Mode Analytics API](http://developer.modeanalytics.com/).

### Installation

```
pip install pymode
```

### Example Usage

```
import pymode

# First create a Mode instance:

# Explicitly setting API token and API password
m = Mode('<your-org-name>','you-mode-api-token','your-mode-api-password')

# API token and API password set as environment variables
m = Mode('<your-org-name>')

for report in m.get_space('<space-token>').get_reports():
    report.run()
```

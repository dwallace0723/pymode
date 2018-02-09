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

# You can explicitly set the API token and API password
m = pymode.Mode('<your-org-name>','<your-mode-api-token>','<your-mode-api-password>')

# Or your API token and API password can be set as environment variables
m = pymode.Mode('<your-org-name>')

# Archive "Untitled Reports" in your Personal space
spaces = m.get_spaces()

for space in spaces:
    if space.name == 'Personal':
        reports = space.get_reports()
        for report in reports:
            if not report.name:
                report.archive()
        break
```

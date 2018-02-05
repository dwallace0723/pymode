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

# Archive "Untitled Reports" in your Personal space
spaces = m.get_spaces()

for space in spaces:
    if space.name == 'Personal':
        reports = space.get_reports()
        for report in reports:
            if not report.name:
                if not report.archived:
                    report.archive()
                else:
                    print('Skipped Report {}: already archived'.format(report.token))
        break
```

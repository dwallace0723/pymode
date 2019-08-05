[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/dwallace0723/pymode.svg?branch=master)](https://travis-ci.com/dwallace0723/pymode)
[![Python Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)](https://pypi.python.org/pypi/ansicolortags/)

## PyMode

PyMode is a Python 3.x library to enable typed interactions with the [Mode Analytics v2 API](http://developer.modeanalytics.com/).

### Installation

```bash
$ pip install pymode
```

### Example Usage

```python
import os
import pymode

ACCOUNT_NAME = os.environ["MODE_ACCOUNT_NAME"]
TOKEN = os.environ["MODE_API_TOKEN"]
PASSWORD = os.environ["MODE_API_PASSWORD"]

mode = pymode.Mode(account_name=MODE_ACCOUNT_NAME, token=TOKEN, password=PASSWORD)

for space in mode.list_spaces():
    for report in mode.list_reports(space_token=space.get('token')):
        print(report.get('name'))
```

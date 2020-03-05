# pymode
[![PyPI version](https://badge.fury.io/py/pymode.svg)](https://badge.fury.io/py/pymode)
![PyPI - Status](https://img.shields.io/pypi/status/pymode)
[![Build Status](https://travis-ci.com/goodeggs/pymode.svg?branch=master)](https://travis-ci.com/goodeggs/pymode.svg?branch=master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymode)
![PyPI - License](https://img.shields.io/pypi/l/pymode)

PyMode is a Python 3.x library to enable typed interactions with the [Mode Analytics v2 API](http://developer.modeanalytics.com/).

### Installation

```bash
$ pip install pymode
```

### Example Usage

```python
import os
from pymode import Mode

ORGANIZATION = os.environ["MODE_ORGANIZATION"]
TOKEN = os.environ["MODE_API_TOKEN"]
PASSWORD = os.environ["MODE_API_PASSWORD"]

mode = Mode(organization=ORGANIZATION, token=TOKEN, password=PASSWORD)
```

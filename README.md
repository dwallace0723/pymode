## PyMode

PyMode is a Python library to enable typed interactions with the [Mode Analytics API](http://developer.modeanalytics.com/).

### Installation

```
pip install pymode
```

### Usage

```
import pymode

m = Mode('<your-org-name>')

for space in m.get_spaces():
    r = space.get_reports()
    print r.name
```

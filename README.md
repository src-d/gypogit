gypogit
=======

gypogit is a wrapper for the awesome [go-git](https://github.com/src-d/go-git) library working with Python 2.7/3.3+/PyPy.

Installation
------------
A wheel may be available for your platform.
```
pip install gypogit
```

To install gypogit from source, you must have a working Go compiler.
```
pip install git+https://github.com/src-d/gypogit
```

Usage
-----
```py
from gypogit import Repository
r = Repository.New("https://github.com/src-d/go-git")
r.PullDefault()
for c in r.Commits():
    print(c)
```
The naming and classes are left intact to match go-git API.

License
-------
MIT.

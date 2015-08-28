commandante
===========

Simple tool for finding forgotten trailing commas in Python expressions.


Why do I even...
----------------
Honestly, this tool won't be of much use to most of users. But there are always will be nitpickers with an axe to grind against superfluous lines in GitHub diffs. Hopefully, it will help you deal with them. :)

One of worst offenders is missing trailing comma at the end of the collections which are spread across multiple lines. Adding new items to them involves adding comma to previous line and this shows in diff.


Installation
------------

    pip install commandante


Running tests
-------------

    pip install pytest
    py.test tests
    
Usage
-----

    bash-3.2$ commandante 1.py main.py test.py
    main.py:45:72: Y001 missing trailing comma
    test.py:46:12: Y001 missing trailing comma


Options
-------

`--autofix`

Attempt to insert missing commas upon detection.

**Example:**

    bash-3.2$ cat test.py
    a = (
        1,
        2
    )
    
    bash-3.2$ commandante --autofix test.py
    bash-3.2$ cat test.py
    a = (
        1,
        2,
    )

License
-------

MIT, man.

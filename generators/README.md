# generators for the files in this repository

Most of the files in this repository have been adapted and updated by hand.
Since that isn't a scalable approach for the future
(and not really work that's transferable to another person),
I've started implementing automatic generators for the settings files.

## `generate-autostart.py`

This python script can generate the `Pantheon` version
of the needed autostart entries automatically.
It depends on features of `python3` version `3.6` or newer.

Usage is pretty simple.
Sane default values are assumed when no arguments are supplied (see below).

```
usage: generate-autostart.py [-h] [--origin ORIGIN]
                             [--suffix SUFFIX]
                             [--destination DESTINATION]
                             [component [component ...]]

positional arguments:
  component                                     override component list (accepts multiple .desktop IDs)

optional arguments:
  -h, --help                                    show this help message and exit
  --origin ORIGIN, -o ORIGIN                    xdg-autostart directory containing original files
  --suffix SUFFIX, -s SUFFIX                    suffix to append to original desktop entry ID
  --destination DESTINATION, -d DESTINATION     output directory for the generated files
```

Default values are:

- `component`: the current list of Pantheon autostart components
- `origin`: `/etc/xdg/autostart/`
- `suffix`: `-pantheon`
- `destination`: current directory


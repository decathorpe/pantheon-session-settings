# generators for the files in this repository

Most of the files in this repository have been adapted and updated by hand.
Since that isn't a scalable approach for the future
(and not really work that's transferable to another person),
I've started implementing automatic generators for the settings files.

The `generate.py` script depends on python version 3.6 or newer,
and optionally uses the `argcomplete` package for bash completion.


## `generate.py applications`

This command will generate the `Pantheon` version
of the Default Applications mapping from the upstream version and
the supplied downstream distribution mapping (`distribution-mappings.json`).

```
usage: generate.py applications [-h]
                                [--upstream UPSTREAM]
                                [--repo REPO]
                                [--destination DESTINATION]
                                [--force]
                                --distribution DISTRIBUTION

required arguments:
  --distribution DISTRIBUTION                   linux distribution to generate a defaults.list for

optional arguments:
  -h, --help                                    show this help message and exit
  --upstream UPSTREAM, -u UPSTREAM              git URL of the upstream repository
  --repo REPO, -r REPO                          upstream git repository path
  --destination DESTINATION, -d DESTINATION     output directory for the generated files
  --force, -f                                   override already existing output files
```

Default values are:

- `upstream`: <https://github.com/elementary/session-settings>
- `repo`: "upstream"
- `destination`: "applications"
- `force`: False


## `generate.py autostart`

This command will generate the `Pantheon` version
of the needed autostart entries automatically.

```
usage: generate-autostart.py [-h]
                             [--origin ORIGIN]
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
- `destination`: "autostart"


## `generate.py gnome-session`

This command will generate the `Pantheon` version
of the GNOME session settings file from the upstream version.

```
usage: generate.py gnome-session [-h]
                                 [--upstream UPSTREAM]
                                 [--repo REPO]
                                 [--destination DESTINATION]
                                 [--force]
                                 [component [component ...]]

positional arguments:
  component                                     override component list (accepts multiple .desktop IDs)

optional arguments:
  -h, --help                                    show this help message and exit
  --upstream UPSTREAM, -u UPSTREAM              git URL of the upstream repository
  --repo REPO, -r REPO                          upstream git repository path
  --destination DESTINATION, -d DESTINATION     output directory for the generated files
  --force, -f                                   override already existing output files
```

Default values are:

- `upstream`: <https://github.com/elementary/session-settings>
- `repo`: "upstream"
- `destination`: "gnome-session"
- `force`: False


## `generate.py xsession`

This command will generate the `Pantheon` version
of the GNOME session settings file from the upstream version.

```
usage: generate.py xsession [-h]
                            [--upstream UPSTREAM]
                            [--repo REPO]
                            [--destination DESTINATION]
                            [--force]

optional arguments:
  -h, --help                                    show this help message and exit
  --upstream UPSTREAM, -u UPSTREAM              git URL of the upstream repository
  --repo REPO, -r REPO                          upstream git repository path
  --destination DESTINATION, -d DESTINATION     output directory for the generated files
  --force, -f                                   override already existing output files
```

Default values are:

- `upstream`: <https://github.com/elementary/session-settings>
- `repo`: "upstream"
- `destination`: "xsession"
- `force`: False


## `distribution-mappings.json`

This file contains a mapping from the default applications on elementaryOS
to applications available on the target distribution.
The top-level keys are what the expected arguments for the `--distribution`
argument for `generate.py applications` look like.


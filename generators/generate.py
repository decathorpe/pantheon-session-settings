#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

import abc
import argparse
import configparser
import json
import os
import pprint
import subprocess

from typing import List, Tuple

try:
    # noinspection PyUnresolvedReferences
    import argcomplete
except ImportError:
    ARGCOMPLETE = False
else:
    ARGCOMPLETE = True

DEFAULT_REPO_URL = "https://github.com/elementary/session-settings"
DEFAULT_REPO_PATH = "upstream"

DEFAULT_AUTOSTART_ORIGIN = os.path.join("/etc", "xdg", "autostart")
DEFAULT_AUTOSTART_SUFFIX = "-pantheon"

DEFAULT_AUTOSTART_COMPONENTS = [
    "gnome-keyring-pkcs11.desktop",
    "gnome-keyring-secrets.desktop",
    "gnome-keyring-ssh.desktop",
    "orca-autostart.desktop",
    "org.gnome.SettingsDaemon.A11ySettings.desktop",
    "org.gnome.SettingsDaemon.Color.desktop",
    "org.gnome.SettingsDaemon.Datetime.desktop",
    "org.gnome.SettingsDaemon.DiskUtilityNotify.desktop",
    "org.gnome.SettingsDaemon.Housekeeping.desktop",
    "org.gnome.SettingsDaemon.Keyboard.desktop",
    "org.gnome.SettingsDaemon.MediaKeys.desktop",
    "org.gnome.SettingsDaemon.Power.desktop",
    "org.gnome.SettingsDaemon.PrintNotifications.desktop",
    "org.gnome.SettingsDaemon.Rfkill.desktop",
    "org.gnome.SettingsDaemon.Sharing.desktop",
    "org.gnome.SettingsDaemon.Smartcard.desktop",
    "org.gnome.SettingsDaemon.Sound.desktop",
    "org.gnome.SettingsDaemon.Wacom.desktop",
    "org.gnome.SettingsDaemon.Wwan.desktop",
    "org.gnome.SettingsDaemon.XSettings.desktop",
    "user-dirs-update-gtk.desktop",
]

DEFAULT_SESSION_COMPONENTS = [
    'gala',
    'gala-daemon',
    'org.gnome.SettingsDaemon.A11ySettings',
    'org.gnome.SettingsDaemon.Color',
    'org.gnome.SettingsDaemon.Datetime',
    'org.gnome.SettingsDaemon.DiskUtilityNotify.desktop',
    'org.gnome.SettingsDaemon.Housekeeping',
    'org.gnome.SettingsDaemon.Keyboard',
    'org.gnome.SettingsDaemon.MediaKeys',
    'org.gnome.SettingsDaemon.Power',
    'org.gnome.SettingsDaemon.PrintNotifications',
    'org.gnome.SettingsDaemon.Rfkill',
    'org.gnome.SettingsDaemon.Sharing',
    'org.gnome.SettingsDaemon.Smartcard',
    'org.gnome.SettingsDaemon.Sound',
    'org.gnome.SettingsDaemon.Wwan',
    'org.gnome.SettingsDaemon.Wacom',
    'org.gnome.SettingsDaemon.XSettings'
]

GNOME_SESSION_FILE_NAME = "pantheon.session"
XSESSION_FILE_NAME = "pantheon.desktop"


def get_args() -> dict:
    parser = argparse.ArgumentParser()
    parser.set_defaults(action=None)

    parsers: argparse._SubParsersAction = parser.add_subparsers()

    applications_parser = parsers.add_parser("applications")
    applications_parser.set_defaults(action="applications")

    applications_parser.add_argument(
        "--upstream", "-u",
        action="store",
        default=DEFAULT_REPO_URL,
        required=False,
        help="git URL of the upstream repository",
    )

    applications_parser.add_argument(
        "--repo", "-r",
        action="store",
        default=DEFAULT_REPO_PATH,
        required=False,
        help="upstream git repository path",
    )

    applications_parser.add_argument(
        "--destination", "-d",
        action="store",
        default=os.path.join(os.getcwd(), "applications"),
        required=False,
        help="output directory for the generated files",
    )

    applications_parser.add_argument(
        "--force", "-f",
        action="store_const",
        const=True,
        default=False,
        required=False,
        help="override already existing output files",
    )

    applications_parser.add_argument(
        "--distribution",
        action="store",
        required=True,
        help="linux distribution to generate a defaults.list for",
    )

    autostart_parser = parsers.add_parser("autostart")
    autostart_parser.set_defaults(action="autostart")

    autostart_parser.add_argument(
        "--origin", "-o",
        action="store",
        default=DEFAULT_AUTOSTART_ORIGIN,
        required=False,
        help="xdg-autostart directory containing original files",
    )

    autostart_parser.add_argument(
        "--suffix", "-s",
        action="store",
        default=DEFAULT_AUTOSTART_SUFFIX,
        required=False,
        help="suffix to append to original desktop entry ID",
    )

    autostart_parser.add_argument(
        "--destination", "-d",
        action="store",
        default=os.path.join(".", "autostart"),
        required=False,
        help="output directory for the generated files",
    )

    autostart_parser.add_argument(
        "--force", "-f",
        action="store_const",
        const=True,
        default=False,
        required=False,
        help="force writing over pre-existing files",
    )

    autostart_parser.add_argument(
        "components",
        action="store",
        type=str,
        nargs="*",
        metavar="component",
        help="override component list (accepts multiple .desktop IDs)"
    )

    gnome_session_parser = parsers.add_parser("gnome-session")
    gnome_session_parser.set_defaults(action="gnome-session")

    gnome_session_parser.add_argument(
        "--upstream", "-u",
        action="store",
        default=DEFAULT_REPO_URL,
        required=False,
        help="git URL of the upstream repository",
    )

    gnome_session_parser.add_argument(
        "--repo", "-r",
        action="store",
        default=DEFAULT_REPO_PATH,
        required=False,
        help="upstream git repository path",
    )

    gnome_session_parser.add_argument(
        "--destination", "-d",
        action="store",
        default=os.path.join(os.getcwd(), "gnome-session"),
        required=False,
        help="output directory for the generated files",
    )

    gnome_session_parser.add_argument(
        "--force", "-f",
        action="store_const",
        const=True,
        default=False,
        required=False,
        help="override already existing output files",
    )

    gnome_session_parser.add_argument(
        "components",
        action="store",
        type=str,
        nargs="*",
        metavar="component",
        help="override component list (accepts multiple .desktop IDs)"
    )

    xsession_parser = parsers.add_parser("xsession")
    xsession_parser.set_defaults(action="xsession")

    xsession_parser.add_argument(
        "--upstream", "-u",
        action="store",
        default=DEFAULT_REPO_URL,
        required=False,
        help="git URL of the upstream repository",
    )

    xsession_parser.add_argument(
        "--repo", "-r",
        action="store",
        default=DEFAULT_REPO_PATH,
        required=False,
        help="upstream git repository path",
    )

    xsession_parser.add_argument(
        "--destination", "-d",
        action="store",
        default=os.path.join(os.getcwd(), "xsessions"),
        required=False,
        help="output directory for the generated files",
    )

    xsession_parser.add_argument(
        "--force", "-f",
        action="store_const",
        const=True,
        default=False,
        required=False,
        help="override already existing output files",
    )

    if ARGCOMPLETE:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    return vars(args)


class DesktopFile(configparser.ConfigParser):
    _interpolation = None
    optionxform = (lambda self, option: option)

    def write(self, fp, space_around_delimiters=False):
        super().write(fp, space_around_delimiters)

    @staticmethod
    def from_file(path: str) -> 'DesktopFile':
        desktop = DesktopFile()
        read = desktop.read(path)

        if path not in read:
            raise configparser.ParsingError()

        return desktop


def clone_upstream_repo(path: str, dest: str):
    if os.path.exists(dest) and os.path.exists(os.path.join(dest, ".git")):
        print("upstream repository was already cloned.")
        return

    ret = subprocess.run(
        ["git", "clone", path, dest],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    ret.check_returncode()


class Generator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self) -> int:
        pass


class ApplicationsGenerator(Generator):
    APPLICATIONS_DIRECTORY = "applications"
    DEFAULTS_LIST_NAME = "defaults.list"

    def __init__(self, distribution: str, destination: str, upstream: str, repo: str, force: bool):
        self._distribution = distribution
        self._destination = destination
        self._upstream = upstream
        self._repo = repo
        self._force = force

    @property
    def distribution(self) -> str:
        return self._distribution

    @property
    def destination(self) -> str:
        return self._destination

    @property
    def upstream(self) -> str:
        return self._upstream

    @property
    def repo(self):
        return self._repo

    @property
    def force(self):
        return self._force

    def generate(self) -> int:
        try:
            clone_upstream_repo(self.upstream, self.repo)
        except subprocess.CalledProcessError as e:
            print(e)
            return 1

        defaults_list_path = os.path.join(DEFAULT_REPO_PATH,
                                          self.APPLICATIONS_DIRECTORY,
                                          self.DEFAULTS_LIST_NAME)

        # open upstream version of file
        desktop = DesktopFile.from_file(defaults_list_path)

        upstream_mapping = dict(desktop["Default Applications"])

        # generate upstream mapping of applications to MIME types
        apps = dict()
        for mime in upstream_mapping:
            if upstream_mapping[mime] not in apps.keys():
                apps[upstream_mapping[mime]] = list()

            apps[upstream_mapping[mime]].append(mime)

        # read downstream application mapping
        with open("distribution-mappings.json", "r") as f:
            distribution_mappings = json.loads(f.read())

        try:
            distribution_mapping = distribution_mappings[self.distribution]
        except KeyError:
            print(f"Distribution {self.distribution} is not supported.")
            return 1

        # generate distribution-specific mapping
        downstream_mapping = dict()

        for mime in upstream_mapping.keys():
            application = upstream_mapping[mime]

            try:
                downstream_mapping[mime] = distribution_mapping[application]
            except KeyError:
                print(f"No distribution mapping for application {application}.")
                return 1

        # modify upstream file with distribution defaults
        for mime in downstream_mapping.keys():
            application = downstream_mapping[mime]
            desktop.set("Default Applications", mime, application)

        # write out modified file
        outfile = os.path.join(self.destination, self.DEFAULTS_LIST_NAME)

        if os.path.exists(outfile) and not self.force:
            raise FileExistsError("Destionation file already exists.")

        if not os.path.exists(self.destination):
            os.makedirs(self.destination)

        with open(outfile, "w") as f:
            desktop.write(f)

        return 0


def applications_action(args: dict) -> int:
    if not os.path.isabs(args["destination"]):
        dest = os.path.abspath(args["destination"])
    else:
        dest = args["destination"]

    distribution: str = args["distribution"]
    upstream: str = args["upstream"]
    repo: str = args["repo"]
    force: bool = args["force"]

    generator = ApplicationsGenerator(distribution, dest, upstream, repo, force)
    return generator.generate()


class AutostartGenerator(Generator):
    def __init__(self, origin: str, components: List[str], suffix: str, dest: str, force: bool):
        self._origin = origin
        self._components = components
        self._suffix = suffix
        self._dest = dest
        self._force = force

    @property
    def origin(self) -> str:
        return self._origin

    @property
    def components(self) -> List[str]:
        return self._components

    @property
    def suffix(self) -> str:
        return self._suffix

    @property
    def dest(self) -> str:
        return self._dest

    @property
    def force(self) -> bool:
        return self._force

    def _original_path(self, component: str) -> str:
        return os.path.join(self.origin, component)

    def _output_path(self, component: str) -> str:
        return os.path.join(self.dest,
                            ".".join(os.path.splitext(component)[:-1]) + self.suffix + ".desktop")

    def _check_existence(self, component: str) -> bool:
        return os.path.exists(self._original_path(component))

    def _self_check(self) -> Tuple[List[str], List[str]]:
        present = list()
        missing = list()

        for component in self.components:
            if os.path.exists(self._original_path(component)):
                present.append(component)
            else:
                missing.append(component)

        return present, missing

    def generate(self) -> int:
        present, missing = self._self_check()

        if not present:
            print("No .desktop files found for the specified autostart components.")
            return 1

        if not os.path.exists(self.dest):
            os.makedirs(self.dest)

        if missing:
            print("Some .desktop files for the specified autostart components were not found.")
            print("Use results with caution.")

        # check and modify all upstream components
        for component in self.components:
            desktop = DesktopFile.from_file(self._original_path(component))
            outfile = self._output_path(component)

            if os.path.exists(outfile) and not self.force:
                print("This output file already exists:")
                print(f"  {outfile}")
                print("Consider running with '--force' to overwrite.")
                return 1

            # replace values for OnlyShowIn keys as necessary
            for section in desktop.sections():
                if desktop.has_option(section, "OnlyShowIn"):
                    desktop.set(section, "OnlyShowIn", "Pantheon;")
                if desktop.has_option(section, "NotShowIn"):
                    raise NotImplementedError("Support for 'NotShowIn' isn't implemented yet.")

            # write out modified file
            with open(outfile, "w") as f:
                desktop.write(f)

        if missing:
            print("Skipped components (missing input files):")
            pprint.pprint(missing)

        return 0


def autostart_action(args: dict) -> int:
    if args["components"]:
        components: List[str] = args["components"]
    else:
        components: List[str] = DEFAULT_AUTOSTART_COMPONENTS

    origin: str = args["origin"]
    suffix: str = args["suffix"]
    dest: str = args["destination"]
    force: bool = args["force"]

    generator = AutostartGenerator(origin, components, suffix, dest, force)
    return generator.generate()


class GnomeSessionGenerator(Generator):
    def __init__(self, components: List[str], destination: str,
                 upstream: str, repo: str, force: bool):

        self._components = components
        self._destination = destination
        self._upstream = upstream
        self._repo = repo
        self._force = force

    @property
    def components(self) -> List[str]:
        return self._components

    @property
    def destination(self) -> str:
        return self._destination

    @property
    def upstream(self) -> str:
        return self._upstream

    @property
    def repo(self):
        return self._repo

    @property
    def force(self):
        return self._force

    def generate(self) -> int:
        if not os.path.exists(self.destination):
            os.makedirs(self.destination)

        try:
            clone_upstream_repo(self.upstream, self.repo)
        except subprocess.CalledProcessError as e:
            print(e)
            return 1

        # open upstream version of file
        upstream_session_path = os.path.join(self.repo, "gnome-session", GNOME_SESSION_FILE_NAME)

        upstream_session = DesktopFile.from_file(upstream_session_path)

        # replace "ubuntu" fallback session with "GNOME"
        if upstream_session.has_option("GNOME Session", "FallbackSession"):
            if upstream_session.get("GNOME Session", "FallbackSession") == "ubuntu":
                upstream_session.set("GNOME Session", "FallbackSession", "GNOME")

        # check and compare required components
        req_comps = upstream_session.get("GNOME Session", "RequiredComponents").split(";")[0:-1]

        for def_comp in self.components:
            if def_comp not in req_comps:
                print(f"Default component {def_comp} not present in .session file.")

        for req_comp in req_comps:
            if req_comp not in self.components:
                print(f"Required component {req_comp} not present in default components.")

        # write out modified file
        outfile = os.path.join(self.destination, GNOME_SESSION_FILE_NAME)

        if os.path.exists(outfile) and not self.force:
            raise FileExistsError("Destionation file already exists.")

        with open(outfile, "w") as f:
            upstream_session.write(f)

        return 0


def gnome_session_action(args: dict) -> int:
    if args["components"]:
        components: List[str] = args["components"]
    else:
        components: List[str] = DEFAULT_SESSION_COMPONENTS

    if not os.path.isabs(args["destination"]):
        dest = os.path.abspath(args["destination"])
    else:
        dest = args["destination"]

    upstream: str = args["upstream"]
    repo: str = args["repo"]
    force: bool = args["force"]

    generator = GnomeSessionGenerator(components, dest, upstream, repo, force)
    return generator.generate()


class XSessionGenerator(Generator):
    def __init__(self, destination: str, upstream: str, repo: str, force: bool):
        self._destination = destination
        self._upstream = upstream
        self._repo = repo
        self._force = force

    @property
    def destination(self) -> str:
        return self._destination

    @property
    def upstream(self) -> str:
        return self._upstream

    @property
    def repo(self):
        return self._repo

    @property
    def force(self):
        return self._force

    def generate(self) -> int:
        if not os.path.exists(self.destination):
            os.makedirs(self.destination)

        try:
            clone_upstream_repo(self.upstream, self.repo)
        except subprocess.CalledProcessError as e:
            print(e)
            return 1

        # open upstream version of file
        upstream_xsession_path = os.path.join(self.repo, "xsessions", XSESSION_FILE_NAME)

        upstream_xsession = DesktopFile.from_file(upstream_xsession_path)

        # There's nothing to change in this file - I think
        # TODO: TryExec=wingpanel seems ... weird

        # write out modified file
        outfile = os.path.join(self.destination, XSESSION_FILE_NAME)

        if os.path.exists(outfile) and not self.force:
            raise FileExistsError("Destionation file already exists.")

        with open(outfile, "w") as f:
            upstream_xsession.write(f)

        return 0


def xsession_action(args: dict) -> int:
    if not os.path.isabs(args["destination"]):
        dest = os.path.abspath(args["destination"])
    else:
        dest = args["destination"]

    upstream: str = args["upstream"]
    repo: str = args["repo"]
    force: bool = args["force"]

    generator = XSessionGenerator(dest, upstream, repo, force)
    return generator.generate()


def main() -> int:
    args = get_args()

    action = args["action"]

    if action is None:
        print("No action specified. Exiting.")
        return 1

    actions = {
        "applications": applications_action,
        "autostart": autostart_action,
        "gnome-session": gnome_session_action,
        "xsession": xsession_action
    }

    return actions[action](args)


if __name__ == "__main__":
    exit(main())

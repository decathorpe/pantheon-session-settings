#!/usr/bin/python3

import argparse
import configparser
import os
import pprint

from typing import Dict, List, Tuple


DEFAULT_ORIGIN = os.path.join("/etc", "xdg", "autostart")
DEFAULT_SUFFIX = "-pantheon"

DEFAULT_COMPONENTS = [
    "gnome-keyring-pkcs11.desktop",
    "gnome-keyring-secrets.desktop",
    "gnome-keyring-ssh.desktop",
    "orca-autostart.desktop",
    "org.gnome.SettingsDaemon.A11ySettings.desktop",
    "org.gnome.SettingsDaemon.Clipboard.desktop",
    "org.gnome.SettingsDaemon.Color.desktop",
    "org.gnome.SettingsDaemon.Datetime.desktop",
    "org.gnome.SettingsDaemon.DiskUtilityNotify.desktop",
    "org.gnome.SettingsDaemon.Housekeeping.desktop",
    "org.gnome.SettingsDaemon.Keyboard.desktop",
    "org.gnome.SettingsDaemon.MediaKeys.desktop",
    "org.gnome.SettingsDaemon.Mouse.desktop",
    "org.gnome.SettingsDaemon.Power.desktop",
    "org.gnome.SettingsDaemon.PrintNotifications.desktop",
    "org.gnome.SettingsDaemon.Rfkill.desktop",
    "org.gnome.SettingsDaemon.Sharing.desktop",
    "org.gnome.SettingsDaemon.Smartcard.desktop",
    "org.gnome.SettingsDaemon.Sound.desktop",
    "org.gnome.SettingsDaemon.Wacom.desktop",
    "org.gnome.SettingsDaemon.XSettings.desktop",
    "user-dirs-update-gtk.desktop",
]


class DesktopFile(configparser.ConfigParser):
    _interpolation = None
    optionxform = (lambda self, option: option)


def get_args() -> Dict[str, str]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--origin", "-o",
        action="store",
        default=DEFAULT_ORIGIN,
        required=False,
        help="xdg-autostart directory containing original files",
    )

    parser.add_argument(
        "--suffix", "-s",
        action="store",
        default=DEFAULT_SUFFIX,
        required=False,
        help="suffix to append to original desktop entry ID",
    )

    parser.add_argument(
        "--destination", "-d",
        action="store",
        default=os.getcwd(),
        required=False,
        help="output directory for the generated files",
    )

    parser.add_argument(
        "components",
        action="store",
        type=str,
        nargs="*",
        metavar="component",
        help="override component list (accepts multiple .desktop IDs)"
    )

    args = parser.parse_args()

    return vars(args)


def get_original_path(component: str, origin: str) -> str:
    return os.path.join(origin, component)


def check_existence(component_list: List[str], origin: str) -> Tuple[List[str], List[str]]:
    present = list()
    missing = list()

    for component in component_list:
        if os.path.exists(get_original_path(component, origin)):
            present.append(component)
        else:
            missing.append(component)

    return present, missing


def read_desktop_file(path: str) -> DesktopFile:
    desktop = DesktopFile()
    read = desktop.read(path)

    if path not in read:
        raise configparser.ParsingError()

    return desktop


def main() -> int:
    args = get_args()

    if args["components"]:
        components = args["components"]
    else:
        components = DEFAULT_COMPONENTS

    origin = args["origin"]
    suffix = args["suffix"]

    if not os.path.isabs(args["destination"]):
        destination = os.path.abspath(args["destination"])
    else:
        destination = args["destination"]

    present, missing = check_existence(components, origin)

    if missing:
        if not present:
            print("None of the specified components could be found. Exiting.")
            return 1
        if present:
            print("Some of the specified components could be found.")
            print("Use results with caution.")

    for component in present:
        desktop = read_desktop_file(os.path.join(origin, component))
        outfile = os.path.join(destination, os.path.splitext(component)[0] + suffix + ".desktop")

        if os.path.exists(outfile):
            raise FileExistsError("The output file already exists, and will not be touched.")

        for section in desktop.sections():
            if desktop.has_option(section, "OnlyShowIn"):
                desktop.set(section, "OnlyShowIn", "Pantheon;")
            if desktop.has_option(section, "NotShowIn"):
                raise NotImplementedError("Support for 'NotShowIn' isn't implemented yet.")

        with open(outfile, "w") as f:
            desktop.write(f, space_around_delimiters=False)

        print(f"Processed {component}.")
        print(f"Output file: {outfile}")

    if missing:
        print("Skipped components:")
        pprint.pprint(missing)

    return 0


if __name__ == "__main__":
    exit(main())

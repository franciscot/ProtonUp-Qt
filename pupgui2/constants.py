import os

APP_NAME = 'ProtonUp-Qt'
APP_VERSION = '2.0.0'
ABOUT_TEXT = '''\
GUI for installing/updating Wine/Proton based compatibility tools.

{APP_NAME} v{APP_VERSION} by DavidoTek: https://github.com/DavidoTek/ProtonUp-Qt
Inspired by/partly based on AUNaseef's protonup.

Copyright (C) 2021 DavidoTek, licensed under GPLv3
'''.format(APP_NAME=APP_NAME, APP_VERSION=APP_VERSION)

CONFIG_FILE = os.path.expanduser('~/.config/pupgui/config.ini')
TEMP_DIR = '/tmp/pupgui2.a70200/'

POSSIBLE_INSTALL_LOCATIONS = [
    {'install_dir': '~/.steam/root/compatibilitytools.d/', 'display_name': 'Steam', 'launcher': 'steam'},
    {'install_dir': '~/.var/app/com.valvesoftware.Steam/data/Steam/compatibilitytools.d/', 'display_name': 'Steam Flatpak', 'launcher': 'steam'},
    {'install_dir': '~/.local/share/lutris/runners/wine/', 'display_name': 'Lutris', 'launcher': 'lutris'}
]
"""Configuration parser for nest_m application configurations."""

import os
import sys
import lib

from configparser import ConfigParser


# LOCAL_INI file located at nest_m/config/config.ini
_CORE = sys.modules.get(lib.__name__)
_CORE_PATH = os.path.dirname(os.path.abspath(_CORE.__file__))
LOCAL_INI = os.path.abspath(
    os.path.join(_CORE_PATH, os.pardir, 'config', 'config.ini'))
# SYSTEM_INI file located at /etc/nest_m/config.ini
SYSTEM_INI = os.path.abspath(
    os.path.join(os.path.sep, 'etc', 'nest_m', 'config.ini'))

config = ConfigParser()

# OVERRIDE SYSTEM CONFIG WITH LOCAL
# FIXME off for now
#config.read(SYSTEM_INI)
config.read(LOCAL_INI)
# FIXME log if no configuration detected

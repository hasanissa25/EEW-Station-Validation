from pathlib import Path
from . import _version

ISPAQ_PREF = str(Path(__file__).parent.joinpath(
    'data', 'eew_preferences.txt'))
ISPAQ_PREF_CN = str(Path(__file__).parent.joinpath(
    'data', 'eew_preferences_CN.txt'))
CONFIG = str(Path(__file__).parent.joinpath(
    'data', 'config.ini'))
XML_CONVERTER = str(Path(__file__).parent.joinpath(
    'data', 'stationxml-seed-converter-2.1.0.jar'))
STATION_XML = str(Path(__file__).parent.joinpath(
    'data', 'stationxml.xml'))


__version__ = _version.get_versions()['version']

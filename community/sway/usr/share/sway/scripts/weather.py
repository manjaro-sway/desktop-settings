#!/usr/bin/env python
"""Script for the Waybar weather module."""

import argparse
import json
import locale
import sys
import urllib.parse
import requests
import configparser
from os import path, environ

config_path = path.join(
    environ.get('XDG_CONFIG_HOME') or
    path.join(environ['HOME'], '.config'),
    "weather.cfg"
)

config = configparser.ConfigParser()
config.read(config_path)

# see https://docs.python.org/3/library/locale.html#background-details-hints-tips-and-caveats
locale.setlocale(locale.LC_ALL, "")
current_locale, _ = locale.getlocale(locale.LC_NUMERIC)
city = config.get('DEFAULT', 'city', fallback='auto')
temperature = config.get('DEFAULT', 'temperature', fallback='C')
distance = config.get('DEFAULT', 'distance', fallback='km')
lng = config.get('DEFAULT', 'locale', fallback=locale.getlocale()[0] or current_locale or 'en_US')

if current_locale == "en_US":
    temperature = temperature or "F"
    distance = distance or "miles"

parser = argparse.ArgumentParser(description='Waybar weather module')
parser.add_argument('-t', '--temperature', default=temperature, choices=['C', 'F'],
                    help='Temperature unit: C (Celsius) or F (Fahrenheit)')
parser.add_argument('-d', '--distance', default=distance, choices=['km', 'miles'],
                    help='Distance unit: km or miles')
parser.add_argument('-c', '--city', default=city,
                    help='City name or "auto" for automatic detection')
args = parser.parse_args()

temperature = args.temperature.upper()
distance = args.distance.lower()
city = urllib.parse.quote(args.city)

temperature_unit = "fahrenheit" if temperature == "F" else "celsius"
wind_speed_unit = "mph" if distance == "miles" else "kmh"

try:
    headers = {"Accept-Language": f"{lng.replace('_', '-')},{lng.split('_')[0]};q=0.5"}
    weather = requests.get(f"https://manjaro-sway.download/weather/{city}?temperature_unit={temperature_unit}&wind_speed_unit={wind_speed_unit}", timeout=10, headers=headers).json()
except (
    requests.exceptions.HTTPError,
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
) as err:
    print(str(err))
    sys.exit(1)

print(json.dumps(weather))

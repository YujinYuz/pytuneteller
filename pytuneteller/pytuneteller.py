# -*- coding: utf-8 -*-

"""pytuneteller

Usage:
    pytuneteller (-h | --help)
    pytuneteller horoscope --all [(--yesterday | --today | --tomorrow)]
    pytuneteller horoscope [<sign>]
    pytuneteller horoscope [<sign> (--yesterday | --today | --tomorrow)]


Options:
    -h --help               Show this screen.
    --version               Show version.
    --all                   Displays all signs with their corresponding horoscope of the day.
    --today                 Get horoscope for today.
                            [default: True]
    --yesterday             Get horoscope for yesterday.
                            [default: False]
    --tomorrow              Get horoscope for tomorrow.
                            [default: False]

Examples:
    pytuneteller horoscope --all
    pytuneteller horoscope virgo --today
    pytuneteller horoscope pisces --yesterday
"""


import json
import logging
import random
import requests
import urllib3

from .exceptions import InvalidHoroscope
from .utils import generate_funny_name

from datetime import datetime

from docopt import docopt
from bs4 import BeautifulSoup

# Disable InsecureRequestWarning
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

# Valid horoscope signs
signs = [
    'aries',
    'taurus',
    'gemini',
    'cancer',
    'leo',
    'virgo',
    'libra',
    'scorpio',
    'sagittarius',
    'capricorn',
    'aquarius',
    'pisces'
]


def print_horoscope(horoscope, text, day='today', name=None):

    name = name if name else generate_funny_name()

    format = """
    A fortune has been casted upon you by a {name}!!!
    {horoscope} ({date})
        {text}
    """
    print(format.format(horoscope=horoscope.capitalize(), text=text, date=day, name=name))

def get_horoscope(sign, day='today'):

    def _astrology():
        site = 'https://astrology.com/horoscope/daily/{day}/{sign}.html'.format(sign=sign, day=day)
        h_soup = BeautifulSoup(fetch_request(site).text, 'lxml')
        horoscope = h_soup.find('div', {'class': 'daily-horoscope'}).find('p').text

        return horoscope

    def _ganeshaspeaks():
        d = 'daily' if day == 'today' else day
        site = 'https://www.ganeshaspeaks.com/horoscopes/{day}-horoscope/{sign}/'.format(sign=sign, day=d)
        h_soup = BeautifulSoup(fetch_request(site).text, 'lxml')
        horoscope = h_soup.find('div', {'id': 'daily'}).find('div', {'class': 'row margin-bottom-0'}).find('p').text
        # TODO(yujinyuz): replace Ganesha with a funny name before returning the findings.

        return horoscope

    def _random_horoscope_findings(horoscope_sites=['astrology', 'ganeshaspeaks']):
        rand_choice = random.choice(horoscope_sites)
        random_site = horoscope_site_mapping[rand_choice]
        return random_site()

    horoscope_site_mapping = {
        'astrology': _astrology,
        'ganeshaspeaks': _ganeshaspeaks,
    }

    horoscope_findings = _random_horoscope_findings()

    return horoscope_findings


def fetch_request(url):
    return requests.get(url, verify=False)


def main():
    args = docopt(__doc__)
    sign = args.get('<sign>')
    day = 'today'

    if args.get('--yesterday'):
        day = 'yesterday'
    if args.get('--tomorrow'):
        day = 'tomorrow'
    if sign not in signs:
        raise InvalidHoroscope

    horoscope = get_horoscope(sign, day)
    print_horoscope(sign, horoscope, day)


if __name__ == '__main__':
    main()

# -*- Coding: UTF8 -*-
import math

from ephem import *


zodiac_names = (
    'Aries',
    'Taurus',
    'Gemini',
    'Cancer',
    'Leo',
    'Virgo',
    'Libra',
    'Scorpio',
    'Sagittarius',
    'Capricorn',
    'Aquarius',
    'Pisces',
)

zodiac_elements = (
    'Fire',
    'Earth',
    'Air',
    'Water',
)

zodiac_qualities = (
    'Cardinal',
    'Fixed',
    'Mutable',
)

all_symbols = {
    'Sun': '☉',
    'Moon': '☽',
    'Mercury': '☿',
    'Venus': '♀',
    'Earth': '♁',
    'Mars': '♂',
    'Jupiter': '♃',
    'Saturn': '♄',
    'Uranus': '⛢',
    'Neptune': '♆',
    'Pluto': '♇',

    'Aries': '♈',
    'Taurus': '♉',
    'Gemini': '♊',
    'Cancer': '♋',
    'Leo': '♌',
    'Virgo': '♍',
    'Libra': '♎',
    'Scorpio': '♏',
    'Sagittarius': '♐',
    'Capricorn': '♑',
    'Aquarius': '♒',
    'Pisces': '♓',
}


zodiac_signs = []

for i, name in enumerate(zodiac_names):
    sign = {}
    sign['name'] = name
    sign['index'] = i
    sign['element'] = zodiac_elements[i % 4]
    sign['quality'] = zodiac_qualities[i % 3]
    zodiac_signs.append(sign)


def radians_to_degmin(rad):
    deg = rad * 180 / math.pi
    d = int(deg)
    r = deg - d
    m = int(r * 60)
    return "{}° {}\"".format(d,m)


def get_zodiac_position(body):
    ecl = Ecliptic(body)
    angle = ecl.lon
    sector = int(angle / (2*math.pi / 12))
    angle -= sector * 2 * math.pi / 12
    return (zodiac_names[sector], degrees(angle), ecl.lon)


def get_symbol(name):
    return all_symbols[name]


def get_natal_chart(date):

    bodies = (
        Sun,
        Moon,
        Mercury,
        Venus,
        Mars,
        Jupiter,
        Saturn,
        Uranus,
        Neptune,
        Pluto,
    )

    chart = {}

    for fn in bodies:
        body = fn(date)
        (sign, angle, total_angle) = get_zodiac_position(body)
        chart[body.name] = {
            'sign': sign,
            'total_angle': total_angle,
            'angle': angle,
            'angle_dms': radians_to_degmin(angle),
        }

    return chart

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
	return (zodiac_signs[sector], degrees(angle))

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
		(sign, angle) = get_zodiac_position(body)
		print(angle)
		chart[body.name] = {
			'sign': sign,
			'angle': angle,
			'angle_dms': radians_to_degmin(angle),
		}

	return chart


def birthdays_from_ical(data):
	import re
	import icalendar
	from dateutil import parser
	cal = icalendar.Calendar.from_ical(data)
	folks = []
	for component in cal.walk():
		if component.name == "VEVENT":
			date_str = component.get('dtstart').to_ical()
			date = parser.parse(date_str)
			if date.year is not 1904:
				summary = component.get('summary')
				m = re.match(r"(.*).s Birthday", summary)
				if m:
					name = m.group(1)
					folks.append({
						'date': date,
						'name': name,
					})
	return folks

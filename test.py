from ephem import *
import math
import sys

from astro import birthdays_from_ical

with open('data/Birthdays.ics', 'rb') as f:
	data = f.read()
	folks = birthdays_from_ical(data)

	for folk in folks:
		date = folk['date']
		if date.year > 1904:
			chart = get_chart(folk['date'])

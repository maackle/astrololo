import requests

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask.ext.login import current_user, login_required
from mongoengine.errors import NotUniqueError

import models
from decorators import user_required, owner_required
from util import gridfs_response
import astro

blueprint = Blueprint('user', __name__, template_folder='templates')

@blueprint.route('/')
@login_required
def home():
	return render_template('views/user/home.jade')

@blueprint.route('/import/ical/', methods=['POST'])
@login_required
def import_ical():
	ics = request.files['ics']
	if ics:
		birthdays = astro.birthdays_from_ical(ics.read())
		subjects = tuple(models.Subject(name=person['name'], birthdate=person['date']) for person in birthdays)
		current_user.subjects = subjects
		current_user.save()
		flash('Added {} subjects'.format(len(subjects)))
		return redirect(url_for('user.home'))
	else:
		return "no filez!!"


@blueprint.route('/explore/', methods=['GET'])
@login_required
def explore():
	charts = tuple(s.get_natal_chart() for s in current_user.subjects)
	subjects_with_charts = zip(current_user.subjects, charts)
	return render_template('views/user/explore.jade', subjects=subjects_with_charts, natal_charts=charts, get_symbol=astro.get_symbol)

@blueprint.route('/profile/<user_slug>/')
def profile(user_slug):
	return "PROFILE"
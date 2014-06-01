from functools import wraps

from flask import abort, redirect
from flask.ext.login import current_user

from models import User

def user_required(f):
	'''
	Decorates any route function that takes a <user_slug> parameter.
	If a user with that slug exists, pass it on to the function as a <user> parameter instead.
	If not, throw 404.

	Useful for e.g. publicly available user views.
	'''

	@wraps(f)
	def decorated(*args, **kwargs):
		if 'user_slug' in kwargs:
			slug = kwargs['user_slug']
			user = User.objects(slug=slug).first_or_404()
		if user:
			del kwargs['user_slug']
			kwargs['user'] = user
			return f(*args, **kwargs)
		else:
			abort(404) 
	return decorated



def owner_required(f):
	'''
	Decorates any route function that takes a <user_slug> parameter.
	If a user with that slug exists, AND the current_user matches, pass it on to the function as a <user> parameter instead.
	If not, throw 404.

	Useful for e.g. letting a user manage his own settings.
	'''

	@wraps(f)
	def decorated(*args, **kwargs):
		if 'user_slug' in kwargs:
			slug = kwargs['user_slug']
			user = User.objects(slug=slug).first_or_404()
		if user and current_user.is_authenticated() and user.id == current_user.id:
			del kwargs['user_slug']
			kwargs['user'] = user
			return f(*args, **kwargs)
		else:
			abort(404) 
	return decorated


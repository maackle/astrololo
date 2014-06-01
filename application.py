import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, redirect, session, flash, url_for, g
from flask.ext.assets import Environment, Bundle
from flask.ext.login import current_user
from flask.ext.admin import Admin
import requests
import mongoengine
from flask.ext.mongoengine import MongoEngine


def create_app():

	from cache import cache

	requests.packages.urllib3.add_stderr_logger()

	app = Flask(__name__)

	app.config.from_object('config.settings')
	try:
		app.config.from_envvar('ASTROLOLO_SETTINGS')
		print("Loaded config from envvar ASTROLOLO_SETTINGS")
	except:
		app.config.from_object('config.development')
		print("Loaded DEVELOPMENT config")

	app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

	assets = Environment(app)
	assets.url = app.static_url_path

	cache.init_app(app, config={
		'CACHE_TYPE': 'simple',
		# 'CACHE_DIR': '.flask-cache',
		'CACHE_THRESHOLD': 1000000,
		'CACHE_DEFAULT_TIMEOUT': 60*60*60*24,  # one day
		})

	return app

def create_db(app):

	db = MongoEngine(app)
	return db

def setup_routes(app):
	'''
	Do everything that needs to be done, return everything that needs to be returned
	'''

	from routes.auth import blueprint as auth
	from routes.frontend import blueprint as frontend
	from routes.user import blueprint as user


	from routes.auth import login_manager
	login_manager.init_app(app)

	app.register_blueprint(frontend, url_prefix='')
	app.register_blueprint(auth, url_prefix='/auth')
	app.register_blueprint(user, url_prefix='/user')

	@app.route('/')
	def home():
		return redirect(url_for('frontend.home'))

	@app.route('/login/')
	def login():
		return redirect(url_for('auth.login'))

	@app.route('/logout/')
	def logout():
		return redirect(url_for('auth.logout'))

	@app.route('/images/<image_id>/')
	def image(image_id):
		print(dir(db))
		images = db.images.files
		print(dir(images))


def setup_admin(app):
	from admin import UserAdminView
	admin = Admin(app)
	admin.add_view(UserAdminView())

def setup():
	setup_routes(app)
	setup_admin(app)
	return app

app = create_app()
db = create_db(app)

# if __name__ == '__main__':
# 	# handler = RotatingFileHandler("log/error.log", maxBytes=10000000, backupCount=10)
# 	# handler.setLevel(logging.WARNING)
# 	# app.logger.addHandler(handler)

# 	setup(app)
# 	app.run(debug=True, port=5005)
from flask.ext.login import UserMixin
# from flask.ext.mongoengine import Document
# from mongoengine import *
from mongoengine import signals

from util import slugify
import astro

from application import db

class Subject(db.EmbeddedDocument):

	name = db.StringField(max_length=128, required=True)
	birthdate = db.DateTimeField()

	def get_natal_chart(self):
		return astro.get_natal_chart(self.birthdate)


class User(db.Document, UserMixin):

	def __str__(self):
		return self.full_name

	meta = {
		'allow_inheritance': True,
		'indexes': ['id', 'slug',],
	}

	email = db.StringField(max_length=128, required=True)
	password = db.StringField(max_length=128, required=True)
	full_name = db.StringField(max_length=128, required=True)
	slug = db.StringField(max_length=128, required=True)
	subjects = db.ListField(db.EmbeddedDocumentField(Subject))
	
	def get_id(self):
		return str(self.id)

	@staticmethod
	def authenticate(email, password):
		user = User.objects(email=email, password=password).first()
		return user

	@classmethod
	def pre_save(cls, sender, document, **kwargs):
		document.slug = slugify(document.full_name)
		document.email = document.email.lower()


signals.pre_save.connect(User.pre_save, sender=User)
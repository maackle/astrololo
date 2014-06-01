from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.mongoengine import ModelView
from wtforms.widgets import TextArea

import models
from application import db

class MyModelView(ModelView):

	def __init__(self):
		super(MyModelView, self).__init__(self.model)


class UserAdminView(MyModelView):

	model = models.User

	column_exclude_list = ('password', 'slug')
	form_excluded_columns = ('slug',)


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

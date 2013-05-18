import os
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

class MainController(webapp2.RequestHandler):
    def get(self):

        users_dict = {
            "login_url": users.create_login_url("/dashboard"),
            "logout_url": users.create_logout_url("/"),
        }

        template_values = {
            "user": users.get_current_user(),
            "users_dict": users_dict,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/main.html')
        self.response.write(template.render(path, template_values))
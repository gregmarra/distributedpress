import os
import logging

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from controllers.base_controller import BaseHandler
from helpers.user_bundle import UserBundle

class MainController(BaseHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../templates/main.html')
        self.response.write(template.render(path, self.template_values))

class AboutController(BaseHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../templates/about.html')
        self.response.write(template.render(path, self.template_values))
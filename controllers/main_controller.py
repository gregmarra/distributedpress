import os
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from helpers.user_bundle import UserBundle

class MainController(webapp2.RequestHandler):
    def get(self):
        user_bundle = UserBundle()

        template_values = {
            "user_bundle": user_bundle,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/main.html')
        self.response.write(template.render(path, template_values))

class AboutController(webapp2.RequestHandler):
    def get(self):
        user_bundle = UserBundle()

        template_values = {
            "user_bundle": user_bundle,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/about.html')
        self.response.write(template.render(path, template_values))
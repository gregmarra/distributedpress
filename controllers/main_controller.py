import os
import logging
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

class MainController(webapp2.RequestHandler):
    def get(self):
        template_values = {
            "asdf": "cheese"
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/main.html')
        self.response.write(template.render(path, template_values))
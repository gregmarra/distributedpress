import os
import logging
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from models.printer import Printer

class PrinterAddController(webapp2.RequestHandler):
    def get(self):
        template_values = {}
    
        path = os.path.join(os.path.dirname(__file__), '../templates/printer_add.html')
        self.response.write(template.render(path, template_values))

    def post(self):
        printer = Printer(
            owner_name = self.request.get("owner_name"),
            email = self.request.get("email")
        ).put()

        self.redirect("/printers/list")
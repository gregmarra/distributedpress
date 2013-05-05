import os
import logging
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from models.printer import Printer

class PrinterListController(webapp2.RequestHandler):
    def get(self):
        printers = Printer.query().fetch(10000)

        template_values = {
            "printers": printers
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/printer_list.html')
        self.response.write(template.render(path, template_values))
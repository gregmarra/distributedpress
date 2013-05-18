import os
import logging
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from models.printer import Printer

class PrinterDeleteController(webapp2.RequestHandler):
    def post(self):
        printer = Printer.get_by_id(int(self.request.get("printer_key_id")))
        printer.key.delete()
        self.redirect("/dashboard")
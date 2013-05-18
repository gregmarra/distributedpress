import os
import logging
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from helpers.user_bundle import UserBundle
from models.account import Account
from models.printer import Printer

class AdminPrinterListController(webapp2.RequestHandler):
    def get(self):
        user_bundle = UserBundle()
        if not user_bundle.user:
            return self.redirect(user_bundle.login_url)
        if not user_bundle.is_current_user_admin:
            return self.redirect("/")

        printers = Printer.query().fetch(10000)

        template_values = {
            "printers": printers,
            "user_bundle": user_bundle,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/admin_printer_list.html')
        self.response.write(template.render(path, template_values))
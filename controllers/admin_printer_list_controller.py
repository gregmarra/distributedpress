import os
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from models.account import Account
from models.printer import Printer

class AdminPrinterListController(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/"))
        if not users.is_current_user_admin():
            self.redirect(users.create_login_url("/"))

        printers = Printer.query().fetch(10000)

        template_values = {
            "printers": printers,
            "logout": users.create_logout_url("/"),
            "user": user,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/admin_printer_list.html')
        self.response.write(template.render(path, template_values))
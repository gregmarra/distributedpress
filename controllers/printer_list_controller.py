import os
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from models.account import Account
from models.printer import Printer

class PrinterListController(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            return self.redirect(users.create_login_url("/"))

        account = Account.get_or_insert(user.user_id())
        printers = Printer.query(Printer.owner == account.key).fetch(10000)

        template_values = {
            "printers": printers,
            "user": user,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/printer_list.html')
        self.response.write(template.render(path, template_values))
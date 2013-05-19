import os
import logging

from google.appengine.ext.webapp import template

from controllers.base_controller import BaseHandler
from models.account import Account
from models.printer import Printer

class AdminPrinterListController(BaseHandler):
    def get(self):
        if not self.user_bundle.user:
            return self.redirect(self.user_bundle.login_url)
        if not self.user_bundle.is_current_user_admin:
            return self.redirect("/")

        printers = Printer.query().fetch(10000)

        self.template_values.update({
            "printers": printers,
        })
    
        path = os.path.join(os.path.dirname(__file__), '../templates/admin_printer_list.html')
        self.response.write(template.render(path, self.template_values))
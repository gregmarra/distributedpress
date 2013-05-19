import os
import logging

from google.appengine.ext.webapp import template

from controllers.base_controller import BaseHandler
from models.account import Account
from models.printer import Printer

class AdminPrinterListController(BaseHandler):
    def __init__(self, *args, **kw):
        super(AdminPrinterListController, self).__init__(*args, **kw)
        self._require_admin()

    def get(self):
        printers = Printer.query().fetch(10000)

        self.template_values.update({
            "printers": printers,
        })
    
        path = os.path.join(os.path.dirname(__file__), '../templates/admin_printer_list.html')
        self.response.write(template.render(path, self.template_values))
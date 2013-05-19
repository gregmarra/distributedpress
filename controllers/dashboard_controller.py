import os
import logging

from google.appengine.api import users
from google.appengine.ext.webapp import template

from controllers.base_controller import BaseHandler
from models.account import Account
from models.printer import Printer
from models.print_job import PrintJob

class DashboardController(BaseHandler):
    def __init__(self, *args, **kw):
        super(DashboardController, self).__init__(*args, **kw)
        self._require_login()

    def get(self):
        if not self.user_bundle.user:
            return self.redirect(self.user_bundle.login_url)

        account = Account.get_or_insert(self.user_bundle.user.user_id())
        printers = Printer.query(Printer.owner == account.key).fetch(10000)
        print_jobs = PrintJob.query().fetch(3)

        self.template_values.update({
            "printers": printers,
            "print_jobs": print_jobs,
        })
    
        path = os.path.join(os.path.dirname(__file__), '../templates/dashboard.html')
        self.response.write(template.render(path, self.template_values))
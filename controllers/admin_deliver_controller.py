import httplib2
import logging
import os
import urllib

from google.appengine.ext.webapp import template

from oauth2client.appengine import StorageByKeyName

import ann_config

from controllers.base_controller import BaseHandler
from helpers.print_job_enqueuer import PrintJobEnqueuer
from models.account import Account
from models.printer import Printer
from models.print_job import PrintJob
from models.gcp_credentials import GcpCredentials

class AdminIssueDeliverController(BaseHandler):
    def __init__(self, *args, **kw):
        super(AdminIssueDeliverController, self).__init__(*args, **kw)
        self._require_admin()

    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../templates/admin_deliver.html')
        self.response.write(template.render(path, self.template_values))


    def post(self):
        if self.request.get("deliver_config") == "test":
            self._deliver_test()
        elif self.request.get("deliver_config") == "ship":
            self._deliver_ship()

    def _deliver_ship(self):
        """Ship to everyone"""

        account = Account.get_or_insert(self.user_bundle.user.user_id())
        printers = Printer.query().fetch(1000)

        print_job = PrintJob(
            submitter = account.key,
            title = self.request.get(self.request.get("deliver_title")),
            url = self.request.get("deliver_url"),
        ).put()

        PrintJobEnqueuer.enqueue_to_printers(
            printers,
            self.request.get("deliver_title"),
            self.request.get("deliver_url")
        )

        self.redirect("/dashboard")

    def _deliver_test(self):
        """Print to the admins printer."""

        gcp_cred_storage = StorageByKeyName(GcpCredentials, self.user.user_id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()
        
        if not gcp_creds:
            return self.redirect("/printers/add")
        
        account = Account.get_or_insert(self.user_bundle.user.user_id())
        printers = Printer.query(Printer.owner == account.key).fetch(1000)

        PrintJobEnqueuer.enqueue_to_printers(
            printers,
            self.request.get("deliver_title"),
            self.request.get("deliver_url")
        )

        self.template_values.update({
            "deliver_title": self.request.get("deliver_title"),
            "deliver_url": self.request.get("deliver_url"),
            "printer_names": [printer.display_name for printer in printers]
        })

        path = os.path.join(os.path.dirname(__file__), '../templates/admin_deliver.html')
        self.response.write(template.render(path, self.template_values)) 

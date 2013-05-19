import httplib2
import logging
import os
import urllib

from google.appengine.api import taskqueue
from google.appengine.ext.webapp import template

from oauth2client.appengine import StorageByKeyName

import ann_config

from controllers.base_controller import BaseHandler
from models.account import Account
from models.printer import Printer
from models.gcp_credentials import GcpCredentials

class AdminDeliverController(BaseHandler):
    def __init__(self, *args, **kw):
        super(AdminDeliverController, self).__init__(*args, **kw)
        self._check_is_admin()

    def _check_is_admin(self):
        if not self.user_bundle.user:
            return self.redirect(user_bundle.login_url, abort=True)
        if not self.user_bundle.is_current_user_admin:
            return self.redirect(user_bundle.login_url, abort=True)

    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../templates/admin_deliver.html')
        self.response.write(template.render(path, self.template_values))


    def post(self):
        if self.request.get("deliver_config") == "test":
            gcp_cred_storage = StorageByKeyName(GcpCredentials, self.user.user_id(), 'credentials')
            gcp_creds = gcp_cred_storage.get()
            
            if not gcp_creds:
                return self.redirect("/printers/add")
            
            account = Account.get_or_insert(self.user.user_id())
            printers = Printer.query(Printer.owner == account.key).fetch(1000)

            for printer in printers:
                taskqueue.add(
                    url = "/tasks/print/submit", 
                    method = "POST",
                    params = {
                        "printer_key_id": printer.key.id(),
                        "title": self.request.get("deliver_title"),
                        "url": self.request.get("deliver_url")
                        }
                    )

            self.template_values.update({
                "deliver_url": self.request.get("deliver_url"),
                "deliver_title": self.request.get("deliver_title"),
                "printer_names": [printer.display_name for printer in printers]
            })

            path = os.path.join(os.path.dirname(__file__), '../templates/admin_deliver.html')
            self.response.write(template.render(path, self.template_values))

        elif self.request.get("deliver_config") == "ship":
            
            printers = Printer.query().fetch(1000)

            for printer in printers:
                taskqueue.add(
                    url = "/tasks/print/submit", 
                    method = "POST",
                    params = {
                        "printer_key_id": printer.key.id(),
                        "title": self.request.get("deliver_title"),
                        "url": self.request.get("deliver_url")
                        }
                    )

            self.redirect("/dashboard")        

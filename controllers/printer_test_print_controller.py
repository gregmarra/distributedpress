import httplib2
import logging
import urllib
import webapp2

from google.appengine.api import taskqueue
from google.appengine.api import users
from google.appengine.ext.webapp import template

from oauth2client.appengine import StorageByKeyName

import ann_config

from helpers.user_bundle import UserBundle
from models.printer import Printer
from models.gcp_credentials import GcpCredentials

class PrinterTestPrintController(webapp2.RequestHandler):
    def post(self):
        user_bundle = UserBundle()
        if not user_bundle.user:
            return self.redirect(user_bundle.login_url)

        gcp_cred_storage = StorageByKeyName(GcpCredentials, user_bundle.user.user_id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()

        if not gcp_creds:
            return self.redirect("/printers/add")

        printer = Printer.get_by_id(int(self.request.get("printer_key_id")))

        taskqueue.add(
                    url = "/tasks/print/submit", 
                    method = "POST",
                    params = {
                        "printer_key_id": printer.key.id(),
                        "title": "Cloudfax Test Print",
                        "url": "http://www.google.com"
                        }
                    )
        
        self.redirect("/dashboard")

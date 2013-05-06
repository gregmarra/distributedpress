import httplib2
import logging
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

from oauth2client.appengine import StorageByKeyName

import ann_config

from models.printer import Printer
from models.gcp_credentials import GcpCredentials

class PrinterTestPrintController(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/"))

        gcp_cred_storage = StorageByKeyName(GcpCredentials, user.user_id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()

        if not gcp_creds:
            self.redirect("/printers/add")

        printer = Printer.get_by_id(int(self.request.get("printer_key_id")))

        data = {
            'printerid': printer.cloudprint_id,
            'title': 'apartment news network',
            'content': 'http://www.google.com',
            'contentType': 'url',
        }
        body = urllib.urlencode(data)
        http = gcp_creds.authorize(httplib2.Http())
        resp, content = http.request('https://www.google.com/cloudprint/submit', method="POST", body=body)
        self.response.write(content)

        self.redirect("/printers/list")

import httplib2
import logging
import urllib
import webapp2

from oauth2client.appengine import StorageByKeyName

import ann_config

from models.printer import Printer
from models.gcp_credentials import GcpCredentials

class PrintSubmitTask(webapp2.RequestHandler):
    def get(self):
        printer = Printer.get_by_id(int(self.request.get("printer_key_id")))
        account = printer.owner
        gcp_cred_storage = StorageByKeyName(GcpCredentials, account.id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()

        if not gcp_creds:
            return logging.warning("Missing credentials for %s" % printer)

        data = {
            'printerid': printer.cloudprint_id,
            'title': self.request.get("title"),
            'content': self.request.get("url"),
            'contentType': 'url',
        }
        body = urllib.urlencode(data)
        http = gcp_creds.authorize(httplib2.Http())
        resp, content = http.request('https://www.google.com/cloudprint/submit', method="POST", body=body)
        self.response.write(content)

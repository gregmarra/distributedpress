import httplib2
import json
import logging
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template

from oauth2client.appengine import StorageByKeyName

import ann_config

from controllers.base_controller import BaseHandler
from models.account import Account
from models.gcp_credentials import GcpCredentials
from models.printer import Printer


class PrinterAddController(BaseHandler):
    def __init__(self, *args, **kw):
        super(PrinterAddController, self).__init__(*args, **kw)
        self._require_login()

    @ann_config.oauth_decorator.oauth_aware
    def get(self):
        gcp_cred_storage = StorageByKeyName(GcpCredentials, self.user_bundle.user.user_id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()
        if gcp_creds is None:
            if ann_config.oauth_decorator.has_credentials():
                gcp_creds = ann_config.oauth_decorator.credentials
                gcp_cred_storage.put(gcp_creds)
            else:
                self.template_values.update({
                    "auth_url": ann_config.oauth_decorator.authorize_url(),
                })
                path = os.path.join(os.path.dirname(__file__), '../templates/gcp_authorization_request.html')
                self.response.write(template.render(path, self.template_values))
                return None

        http = gcp_creds.authorize(httplib2.Http())
        resp, content = http.request('http://www.google.com/cloudprint/search')
        
        response_json = json.loads(content)
        printers = response_json["printers"]

        self.template_values.update({
            "printers": printers,
        })
    
        path = os.path.join(os.path.dirname(__file__), '../templates/printer_add.html')
        self.response.write(template.render(path, self.template_values))
        
    def post(self):
        account = Account.get_or_insert(
            self.user_bundle.user.user_id(),
            email = self.user_bundle.user.email(),
            nickname = self.user_bundle.user.nickname())

        printer = Printer(
            owner = account.key,
            cloudprint_id = self.request.get("printer_cloudprint_id"),
            display_name = self.request.get("printer_display_name"),
        ).put()

        return self.redirect("/dashboard")

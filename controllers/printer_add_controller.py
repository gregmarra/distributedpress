import httplib2
import json
import logging
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from oauth2client.appengine import StorageByKeyName

import ann_config

from models.account import Account
from models.gcp_credentials import GcpCredentials
from models.printer import Printer


class PrinterAddController(webapp2.RequestHandler):
    @ann_config.oauth_decorator.oauth_aware
    def get(self):
        user = users.get_current_user()
        if not user:
            return self.redirect(users.create_login_url("/"))

        gcp_cred_storage = StorageByKeyName(GcpCredentials, user.user_id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()
        if gcp_creds is None:
            if ann_config.oauth_decorator.has_credentials():
                gcp_creds = ann_config.oauth_decorator.credentials
                gcp_cred_storage.put(gcp_creds)
            else:
                template_values = {
                    "auth_url": ann_config.oauth_decorator.authorize_url(),
                    "logout": users.create_logout_url("/"),
                    "user": user,
                }
                path = os.path.join(os.path.dirname(__file__), '../templates/gcp_authorization_request.html')
                self.response.write(template.render(path, template_values))
                return None

        http = gcp_creds.authorize(httplib2.Http())
        resp, content = http.request('http://www.google.com/cloudprint/search')
        
        response_json = json.loads(content)
        printers = response_json["printers"]

        template_values = {
            "printers": printers,
            "logout": users.create_logout_url("/"),
            "user": user,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/printer_add.html')
        self.response.write(template.render(path, template_values))
        

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/"))

        account = Account.get_or_insert(
            user.user_id(),
            email = user.email(),
            nickname = user.nickname())

        printer = Printer(
            owner = account.key,
            cloudprint_id = self.request.get("printer_cloudprint_id"),
            display_name = self.request.get("printer_display_name"),
        ).put()

        return self.redirect("/printers/list")

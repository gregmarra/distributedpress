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

from helpers.user_bundle import UserBundle
from models.account import Account
from models.gcp_credentials import GcpCredentials
from models.printer import Printer


class PrinterAddController(webapp2.RequestHandler):
    @ann_config.oauth_decorator.oauth_aware
    def get(self):
        user_bundle = UserBundle()
        if not user_bundle.user:
            return self.redirect(user_bundle.login_url)

        gcp_cred_storage = StorageByKeyName(GcpCredentials, user_bundle.user.user_id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()
        if gcp_creds is None:
            if ann_config.oauth_decorator.has_credentials():
                gcp_creds = ann_config.oauth_decorator.credentials
                gcp_cred_storage.put(gcp_creds)
            else:
                template_values = {
                    "auth_url": ann_config.oauth_decorator.authorize_url(),
                    "user_bundle": user_bundle,
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
            "user_bundle": user_bundle,
        }
    
        path = os.path.join(os.path.dirname(__file__), '../templates/printer_add.html')
        self.response.write(template.render(path, template_values))
        

    def post(self):
        user_bundle = UserBundle()
        if not user_bundle.user:
            return self.redirect(user_bundle.login_url)

        account = Account.get_or_insert(
            user_bundle.user.user_id(),
            email = user_bundle.user.email(),
            nickname = user_bundle.user.nickname())

        printer = Printer(
            owner = account.key,
            cloudprint_id = self.request.get("printer_cloudprint_id"),
            display_name = self.request.get("printer_display_name"),
        ).put()

        return self.redirect("/dashboard")

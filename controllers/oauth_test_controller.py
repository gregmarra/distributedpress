import os
import httplib2
import json
import logging
import webapp2
import urllib

import ann_config

class Oauth2TestController(webapp2.RequestHandler):

    @ann_config.oauth_decorator.oauth_aware
    def get(self):
        if ann_config.oauth_decorator.has_credentials():
            self.response.write("has creds")
            
            http = ann_config.oauth_decorator.credentials.authorize(httplib2.Http())
            resp, content = http.request('http://www.google.com/cloudprint/search')
            self.response.write(content)

            response_json = json.loads(content)
            printerid = response_json["printers"][0]["id"]

            data = {
                'printerid': printerid,
                'title': 'apartment news network',
                'content': 'http://www.google.com',
                'contentType': 'url',
            }
            body = urllib.urlencode(data)
            http = ann_config.oauth_decorator.credentials.authorize(httplib2.Http())
            resp, content = http.request('https://www.google.com/cloudprint/submit', method="POST", body=body)
            self.response.write(content)           
            
            # Write the task data
        else:
            url = ann_config.oauth_decorator.authorize_url()
            self.response.write("no creds. %s" % url)
            # Write a page explaining why authorization is needed,
            # and provide the user with a link to the url to proceed.
            # When the user authorizes, they get redirected back to this path,
            # and has_credentials() returns True.

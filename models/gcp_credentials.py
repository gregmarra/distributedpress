from google.appengine.ext import ndb
from oauth2client.appengine import CredentialsNDBProperty

class GcpCredentials(ndb.Model):
    credentials = CredentialsNDBProperty()
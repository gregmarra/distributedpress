import json

from google.appengine.ext import ndb

class Printer(ndb.Model):
    """
    Printers represent things that should be printed to.
    """
    email = ndb.StringProperty(indexed=False)
    owner_name = ndb.StringProperty(indexed=False) #a json blob
    
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

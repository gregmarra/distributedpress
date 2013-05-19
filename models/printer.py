from google.appengine.ext import ndb

from models.account import Account

class Printer(ndb.Model):
    """
    Printers represent things that should be printed to.
    """
    cloudprint_id = ndb.StringProperty(indexed=False, required=True)
    display_name = ndb.StringProperty()
    owner = ndb.KeyProperty(kind=Account, required=True)
    
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

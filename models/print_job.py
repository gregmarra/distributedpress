from google.appengine.ext import ndb

from models.account import Account

class PrintJob(ndb.Model):
    """
    Accounts represent accounts people use to add and manage printer.
    """
    author = ndb.KeyProperty(kind=Account, required=True)
    title = ndb.StringProperty(required=True)
    url = ndb.StringProperty(required=True)

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

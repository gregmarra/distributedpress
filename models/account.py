from google.appengine.ext import ndb

class Account(ndb.Model):
    """
    Accounts represent accounts people use to add and manage printer.
    """
    email = ndb.StringProperty()
    nickname = ndb.StringProperty()

    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

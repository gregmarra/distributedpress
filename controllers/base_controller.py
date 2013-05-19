import webapp2

from helpers.user_bundle import UserBundle

class BaseHandler(webapp2.RequestHandler):
    """
    Provides a base set of functionality for pages.
    """

    def __init__(self, *args, **kw):
        super(BaseHandler, self).__init__(*args, **kw)
        self.user_bundle = UserBundle()
        self.template_values = {
            "user_bundle": self.user_bundle
        }

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

    def _require_admin(self):
        self._require_login()
        if not self.user_bundle.is_current_user_admin:
            return self.redirect(self.user_bundle.login_url, abort=True)

    def _require_login(self):
        if not self.user_bundle.user:
            return self.redirect(self.user_bundle.login_url, abort=True)
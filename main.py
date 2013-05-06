import webapp2

import ann_config

from controllers.main_controller import MainController
from controllers.oauth_test_controller import Oauth2TestController
from controllers.printer_add_controller import PrinterAddController
from controllers.printer_delete_controller import PrinterDeleteController
from controllers.printer_list_controller import PrinterListController

app = webapp2.WSGIApplication([
    ('/', MainController),
    ('/printers/add', PrinterAddController),
    ('/printers/delete', PrinterDeleteController),
    ('/printers/list', PrinterListController),
    ('/oauth2', Oauth2TestController),
    (ann_config.oauth_decorator.callback_path, ann_config.oauth_decorator.callback_handler()),
], debug=True)

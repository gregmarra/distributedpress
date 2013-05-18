import webapp2

import ann_config

from controllers.admin_deliver_controller import AdminDeliverController
from controllers.admin_printer_list_controller import AdminPrinterListController
from controllers.main_controller import MainController
from controllers.dashboard_controller import DashboardController
from controllers.printer_add_controller import PrinterAddController
from controllers.printer_delete_controller import PrinterDeleteController
from controllers.printer_test_print_controller import PrinterTestPrintController

app = webapp2.WSGIApplication([
    ('/', MainController),
    ('/admin/printers/list', AdminPrinterListController),
    ('/admin/deliver', AdminDeliverController),
    ('/dashboard', DashboardController),
    ('/printers/add', PrinterAddController),
    ('/printers/delete', PrinterDeleteController),
    ('/printers/test', PrinterTestPrintController),
    (ann_config.oauth_decorator.callback_path, ann_config.oauth_decorator.callback_handler()),
], debug=True)

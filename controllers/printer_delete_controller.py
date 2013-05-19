from controllers.base_controller import BaseHandler
from models.printer import Printer

class PrinterDeleteController(BaseHandler):
    def post(self):
        printer = Printer.get_by_id(int(self.request.get("printer_key_id")))
        printer.key.delete()
        self.redirect("/dashboard")
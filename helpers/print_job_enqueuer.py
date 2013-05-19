from google.appengine.api import taskqueue

class PrintJobEnqueuer(object):
    """
    PrintJobEnqueuer puts print jobs on the taskqueue
    """
    @classmethod
    def enqueue_to_printers(self, printers, title, url):
        for printer in printers:
            self.enqueue_to_printer(self, printer, title, url)

    @classmethod
    def enqueue_to_printer(self, printer, title, url):
        taskqueue.add(
                url = "/tasks/print/submit", 
                method = "POST",
                params = {
                    "printer_key_id": printer.key.id(),
                    "title": title,
                    "url": url,
                    }
                )

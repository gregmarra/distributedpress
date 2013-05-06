import webapp2

import ann_config

from tasks.print_submit_task import PrintSubmitTask

app = webapp2.WSGIApplication([
    ('/tasks/print/submit', PrintSubmitTask),
], debug=True)

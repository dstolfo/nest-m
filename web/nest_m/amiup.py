

import tornado.web


class AmIUpHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(self.request.version)

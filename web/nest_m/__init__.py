
import os
import tornado.web

from lib.config import config
from web.nest_m.amiup import AmIUpHandler
from web.nest_m.home import HomeHandler


class NestMApplication(tornado.web.Application):

    def __init__(self):

        handlers = [
            (r"/amiup", AmIUpHandler),
            (r"/", HomeHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


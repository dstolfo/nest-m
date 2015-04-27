

from lib.tornado.web import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        self.render_j("home.html")


from lib.tornado.web import BaseHandler


class CourseSlides1Handler(BaseHandler):

    def get(self):
        self.render_j("course_slides_1.html")

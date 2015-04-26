
import os
import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class TemplateRendering:
    """
    A simple class to hold methods for rendering templates.
    """
    def render_template(self, template_name, **kwargs):

        def static_url(path,**kwargs):
            if kwargs is not None and 'shared' in kwargs and kwargs['shared']:
                return "/static_shared/" + path
            else:
                return "/static/" + path

        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(
                self.settings["template_path"]
            )


        env = Environment(loader=FileSystemLoader(template_dirs))
        env.globals['static_url'] = static_url
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(tornado.web.RequestHandler, TemplateRendering):
    """
    RequestHandler already has a `render()` method. I'm writing another
    method `render_j()` and keeping the API almost same.
    """
    def render_j(self, template_name, **kwargs):
        """
        This is for making some extra context variables available to
        the template
        """
        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)

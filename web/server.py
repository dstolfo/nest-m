
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from lib.config import config

from web.nest_m import NestMApplication

define("port", default=None,
    help="connect web server to given port", type=int)

def main():

    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(
        NestMApplication())
    http_server.listen(options.port or \
        int(config['web_server']['port']))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

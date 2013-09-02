import os
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from raven.contrib.tornado import AsyncSentryClient

define("address", default="localhost", help="run on the given address")
define("port", default=8888, help="run on the given port", type=int)
define("config_file",
       default=os.path.join(
           os.path.dirname(os.path.realpath(__file__)), "config/config.py"),
       help="filename for additional configuration")
define("debug", default=False, group="application",
       help="run in debug mode (with automatic reloading)")
define("sentry_dns", group="application")


class Application(tornado.web.Application):
    def __init__(self, handlers, **settings):
        settings["static_path"] = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "static")

        super(Application, self).__init__(handlers, **settings)

        self.sentry_client = AsyncSentryClient(self.settings["sentry_dns"])


def main(application):
    print("Serving on %s:%s.." % (options.address, options.port))
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

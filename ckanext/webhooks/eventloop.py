import logging
import tornado.web
import tornado.ioloop

from tornado.options import define, options, parse_command_line

define("port", default=8765, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

def main():
    parse_command_line()

    app = tornado.web.Application(
        [
            (r"/", WebhookReceiver)
        ],
        debug = options.debug
    )

    app.listen(options.port)

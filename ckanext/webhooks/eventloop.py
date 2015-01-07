import logging
import requests
import tornado.web
import tornado.ioloop

from tornado.options import define, options, parse_command_line

define("port", default=8765, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

class WebhookReceiver(tornado.web.RequestHandler):

    def post(self):
        import pdb; pdb.set_trace()
        body = self.get_argument("data")
        url = body['address']

        requests.post(url, headers = {
                'Content-Type': 'application/json'
            },
            data = body
        )

def main():
    parse_command_line()

    app = tornado.web.Application(
        [
            (r"/", WebhookReceiver)
        ],
        debug = options.debug
    )

    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

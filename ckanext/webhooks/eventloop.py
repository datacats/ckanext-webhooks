import json
import logging
import tornado.web
import tornado.ioloop

from tornado.options import define, options, parse_command_line
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

define("port", default=8765, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

class WebhookReceiver(tornado.web.RequestHandler):

    def post(self):
        body = json.loads(self.request.body)
        url = body['address']

        httpclient = AsyncHTTPClient()
        request = HTTPRequest(
            url = url,
            method = 'POST',
            headers = {
                'Content-Type': 'application/json'
            },
            body = data
        )

        httpclient.fetch(request, request_handler)

        self.finish()

    def request_handler(self):
        pass

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

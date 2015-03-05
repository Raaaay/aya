# -*- coding: utf-8 -*-
"""
    aya is a tiny web framework written by pure python, which implements WSGI.

"""
from .server import SimpleServer
from .router import Router
from .http import Request, Response


class Aya(object):
    """This class implements central WSGI application object.
    """

    def __init__(self):
        self.router = Router()
        self.request = Request()
        self.response = Response()

    def run(self, host, port, debug=False):
        """
        Run a WSGI server on this server. You can use it like this:
        app = Aya()
        app.run("127.0.0.1", 8080)

        :param host: host or IP.
        :param port: port number.
        :param debug: Is debug switch opened.
        """
        server = SimpleServer(host, port, self)
        server.run()

    def route(self, path, methods=["GET"]):
        """
        The decorator for request route.
        e.g:

        @app.route("/test", methods=["GET", "POST"])
        def test():
            pass

        :param path: request path.
        :param methods: request methods supported.
        :return: a handler wrapper.
        """
        def wrapper(func):
            self.router.add_rule(path, methods, func)
        return wrapper

    def set_header(self, key, value):
        """
        Set the response headers for this request.
        :param key: response header's key.
        :param value: response header's value
        """
        self.response.set_header(key, value)

    def _handle_request(self, handler, args=None):
        try:
            if args:
                ret = handler(**args)
            else:
                ret = handler()
            if isinstance(ret, tuple):
                self.response.set_status(ret[0])
                self.response.set_response_body(ret[1])
            elif isinstance(ret, Response):
                self.response = ret
            else:
                self.response.set_status(200)
                self.response.set_response_body(str(ret))
        except Exception as e:
            self.response.set_status(500)
            self.response.set_response_body(str(e))

    def __call__(self, environ, start_response):
        self.request.set_environ(environ)
        handler, args = self.router.get_handler(self.request.request_path, self.request.request_method)
        if handler:
            self._handle_request(handler, args)
        else:
            self.response.set_status(404)
            self.response.set_response_body("No request handler found.")
        start_response(self.response.status_line, self.response.header.to_list())
        return [self.response.response_body]
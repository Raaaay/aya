# -*- coding: utf-8 -*-
"""
    aya is a tiny web framework written by pure python, which implements WSGI.

"""
from .server import SimpleServer
from .router import Router
from .http import Request, Response, HttpCode


class Aya(object):
    """This class implements central WSGI application object.
    """

    def __init__(self):
        self.router = Router()
        self.request = Request()
        self.response = Response()

    def run(self, host, port, debug=False):
        server = SimpleServer(host, port, self)
        server.run()

    def route(self, path, methods=["GET"]):
        def wrapper(func):
            self.router.add_rule(path, methods, func)
        return wrapper

    def set_response_headers(self, header):
        self.response.set_headers(header)

    def __call__(self, environ, start_response):
        self.request.set_environ(environ)
        func = self.router.get_handler(self.request.request_path, self.request.request_method)
        if func:
            status, data = func()
            self.response.set_status(status)
            self.response.set_response_body(str(data))
        start_response(
            str(self.response.status) + " " + HttpCode.get_status_message(self.response.status),
            self.response.header.to_list())
        return [self.response.response_body]
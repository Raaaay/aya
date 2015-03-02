# -*- coding: utf-8 -*-
"""
    aya is a tiny web framework written by pure python, which implements WSGI.

"""
from .server import SimpleServer
from .router import Router


class Aya(object):
    """This class implements central WSGI application object.
    """

    def __init__(self):
        self.router = Router()

    def run(self, host, port, debug=False):
        server = SimpleServer(host, port, self)
        server.run()

    def route(self, path, method=["GET"]):
        def wrapper(func):
            self.router.add_rule(path, func)
        return wrapper

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        func = self.router.get_handler(path)
        if func:
            func()
        start_response("200 OK", [("location", "http://www.baidu.com")])
        return ["hello, world"]
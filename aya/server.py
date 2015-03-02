# -*- coding: utf-8 -*-
"""
    This module creates a WSGI server for framework.

"""
from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import WSGIRequestHandler


class AbstractClassError(Exception):
    """Raise this Exception when trying to create an instance of an abstract class.
    """
    pass


class BaseServer(object):

    def __init__(self, host, port, app):
        self.host = host
        self.port = port
        self.app = app
        self.server_class = WSGIServer
        self.handler_class = WSGIRequestHandler

    def set_server_class(self, server_class):
        self.server_class = server_class

    def set_handler_class(self, handler_class):
        self.handler_class = handler_class

    def run(self):
        raise AbstractClassError("Abstract class can't have any instance.")


class SimpleServer(BaseServer):

    def run(self):
        server = make_server(self.host, self.port, self.app, self.server_class, self.handler_class)
        server.serve_forever()
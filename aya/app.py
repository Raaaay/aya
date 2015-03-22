# -*- coding: utf-8 -*-
"""
    aya is a tiny web framework written by pure python, which implements WSGI.

"""
import re
import os
import mimetypes

from .server import SimpleServer
from .router import Router
from .http import Request, Response, Cookie


class Aya(object):
    """This class implements central WSGI application object.
    """

    def __init__(self):
        self.router = Router()
        self.request = Request()
        self.response = Response()
        self.static_root = os.path.abspath(os.curdir)

    def set_static_root(self, root):
        """
        Set the root path of static resources.
        :param root: root path of static resources.
        """
        self.static_root = root

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

    def set_cookie(self, key, value):
        """
        Set Cookie for response.
        :param key: Cookie's key
        :param value: Cookie's value
        """
        self.response.set_cookie(key, value)

    def set_response_cookie_info(self, **kwargs):
        """
        Set cookie info for response.
        :param kwargs: cookie's info, include domain, path, and expires.
        """
        self.response.set_cookie_info(**kwargs)

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

    def __is_static(self):
        if re.match("/?static/.+", self.request.request_path):
            return True
        return False

    def __get_content_type(self):
        default_content_type = "text/plain"
        content_type = mimetypes.guess_type(self.request.request_path)[0]
        if content_type:
            return content_type
        return default_content_type

    def handle_static(self, path):
        """
        Handler for static resources.
        :param path: static resource's path
        :return: static content
        """
        abs_path = os.path.join(self.static_root, path.lstrip("/"))
        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            return 404, "Not Found."
        with open(abs_path, "rb") as f:
            return 200, f.read()

    def __call__(self, environ, start_response):
        self.request.set_environ(environ)
        if self.__is_static():
            handler, args = self.handle_static, {"path": self.request.request_path}
        else:
            handler, args = self.router.get_handler(
                self.request.request_path, self.request.request_method)
        if handler:
            self._handle_request(handler, args)
        else:
            self.response.set_status(404)
            self.response.set_response_body("No request handler found.")
        self.response.set_content_type(self.__get_content_type())
        start_response(self.response.status_line, self.response.header.to_list())
        return [self.response.response_body]
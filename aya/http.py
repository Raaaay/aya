# -*- coding: utf-8 -*-
"""
    This module supplies some classes to handle http request.

"""
import threading
import urlparse


class HttpCode(object):
    STAT_MSG_MAP = {
        200: "OK",
        404: "NOT FOUND",
        500: "SERVER ERROR",
        503: "TIME OUT"
    }

    @staticmethod
    def get_status_message(status):
        return HttpCode.STAT_MSG_MAP.get(status, "NOT FOUND")


class Request(threading.local):

    def __init__(self, environ=None):
        self.environ = environ
        if environ:
            self.GET = self.__init_get()
            self.POST = self.__init_post()

    def __init_get(self):
        query = self.environ.get("QUERY_STRING", None)
        if query:
            return self.__parse_query(query)
        return dict()

    def __parse_query(self, query):
        ret = urlparse.parse_qs(query)
        for (key, value) in ret.items():
            ret[key] = value[0] if len(value) == 1 else value
        return ret

    def __init_post(self):
        try:
            content_length = int(self.environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            content_length = 0
        request_body = self.environ["wsgi.input"].read(content_length)
        if request_body:
            return self.__parse_query(request_body)
        return dict()

    def set_environ(self, environ):
        """
        Set the environ of this request.
        :param environ: One dict include environ variables.
        """
        self.environ = environ
        self.__init_get()
        self.__init_post()

    @property
    def request_path(self):
        """
        The path of this request.
        :return: path of this request.
        """
        return self.environ.get("PATH_INFO", None)

    @property
    def params(self):
        """
        All GET and POST parameters of this request.
        :return: All parameters of this request. If one parameter is included both in GET and POST,
        return the POST one.
        """
        return dict(self.GET, **self.POST)

    @property
    def request_method(self):
        """
        Get the request method.
        :return: Request method.
        """
        return self.environ.get("REQUEST_METHOD", "GET")


class Response(threading.local):

    DEFAULT_STATUS = 200

    def __init__(self):
        self.header = Header()
        self.response_body = None
        self.status = Response.DEFAULT_STATUS

    def set_response_body(self, body):
        self.response_body = str(body)

    def set_header(self, header):
        if isinstance(header, dict):
            self.headers.set_data(header)
        elif isinstance(header, Header):
            self.header = header

    def set_status(self, status):
        self.status = status


class Header(threading.local):

    def __init__(self, data=None):
        self.data = data

    def set_data(self, data):
        self.data = data

    def to_list(self):
        return [] if not self.data else [(key, value) for (key, value) in self.data.items()]


class Cookie(threading.local):
    pass
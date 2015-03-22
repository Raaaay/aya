# -*- coding: utf-8 -*-
"""
    This module supplies some classes to handle http request.

"""
import threading
import urlparse
import httplib


class Request(threading.local):
    """
    Http Request class.
    """

    def __init__(self, environ=None):
        self.environ = environ
        self.request_body = None
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
        self.request_body = self.environ["wsgi.input"].read(content_length)
        if self.request_body:
            return self.__parse_query(self.request_body)
        return dict()

    def set_environ(self, environ):
        """
        Set the environ of this request.
        :param environ: One dict include environ variables.
        """
        self.environ = environ
        self.__init_get()
        self.__init_post()

    def get_body(self):
        """
        Get the raw request body of this request.
        :return: request body as string or None
        """
        return self.request_body

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
    """
    Http Response class.
    """

    DEFAULT_STATUS = 200

    def __init__(self):
        self.header = Header()
        self.response_body = None
        self.status = Response.DEFAULT_STATUS

    def set_response_body(self, body):
        """
        Set the body of this response.
        :param body: response body, should be a string, or will be cast to a string.
        """
        self.response_body = str(body)

    def set_header(self, key, value):
        """
        Add one header into this response.
        :param key: key of header.
        :param value: value of header.
        """
        self.header.set_header(key, value)

    def set_content_type(self, content_type):
        """
        Set the content type of response.
        :param content_type: content type
        """
        self.set_header("Content-Type", content_type)

    def set_cookie(self, key, value):
        """
        Set Cookie for response.
        :param key: cookie's key
        :param value: cookie's value
        """
        self.header.set_cookie(key, value)

    def set_cookie_info(self, **kwargs):
        """
        Set cookie info for response.
        :param kwargs: cookie's info, include domain, path, and expires.
        """
        self.header.set_cookie_info(**kwargs)

    def set_status(self, status):
        """
        Set the response code of this response.
        :param status: response code, should be a int like 200, 300...
        """
        self.status = status

    @property
    def status_line(self):
        """
        The status line in response header.
        :return:The status line of this response, like "404 Not Found"
        """
        return " ".join([str(self.status), httplib.responses.get(self.status)])


class Header(threading.local):
    """
    Http header class.
    """

    def __init__(self, data=None):
        self.data = data if isinstance(data, dict) else dict()
        self.cookie = Cookie()

    def set_header(self, key, value):
        """
        Set a header value.
        :param key: key of header. key should be a string.
        :param value: value of header. value will be cast to a string.
        """
        if not isinstance(key, str):
            raise TypeError("header key should be a string.")
        self.data[key] = str(value)

    def set_cookie(self, key, value):
        """
        Set Cookie for response.
        :param key: cookie's key
        :param value: cookie's value
        """
        self.cookie.set_cookie(key, value)

    def set_cookie_info(self, **kwargs):
        """
        Set cookie info for response.
        :param kwargs: cookie's info, include domain, path, and expires.
        """
        if "domain" in kwargs:
            self.cookie.set_domain(kwargs["domain"])
        if "path" in kwargs:
            self.cookie.set_path(kwargs["path"])
        if "expires" in kwargs:
            self.cookie.set_expires(kwargs["expires"])

    def to_list(self):
        """
        Return all headers as a list.
        :return: A list like [(key1, value1), (key2, value2)...]
        """
        if self.cookie.data:
            self.data["Set-Cookie"] = str(self.cookie)
        return [(key, value) for (key, value) in self.data.items()]


class Cookie(threading.local):
    """
    Http Cookie class.
    """
    def __init__(self, path=None, domain=None, expires=None):
        self.data = dict()
        self.path = path
        self.domain = domain
        self.expires = expires

    def set_cookie(self, key, value):
        """
        Set one cookie.
        :param key: key of this cookie
        :param value: value of this cookie
        """
        assert(isinstance(key, str))
        assert(isinstance(value, str))
        self.data[key] = value

    def set_expires(self, expires):
        """
        Set the expire time of this cookie.
        :param expires: expire time of this cookie.
        """
        self.expires = expires

    def set_path(self, path):
        """
        Set the path of this cookie.
        :param path: path of this cookie.
        """
        self.path = path

    def set_domain(self, domain):
        """
        Set domain for this cookie.
        :param domain: domain of this cookie
        """
        self.domain = domain

    def __str__(self):
        if not self.data:
            return ""
        else:
            cookies_str = ";".join([key + "=" + value for (key, value) in self.data.items()])
            if self.path:
                cookies_str += ";path=" + self.path
            if self.domain:
                cookies_str += ";domain=" + self.domain
            if self.expires:
                cookies_str += ";expires=" + self.expires
            cookies_str += ";"
            return cookies_str
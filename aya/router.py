# -*- coding: utf-8 -*-
"""
    Url router for requests.
"""
import re


class Router(object):
    """
    Router for http request.
    You can use arguments in yours urls, like these examples below:

    @app.route("/index", methods=["GET"]) # http://127.0.0.1/index/test

    @app.route("/index/<name>/<int:age>") # http://127.0.0.1/index/chenrui/28

    And you can use argument accuracy to decide to use accuracy match or not.
    If accuracy is False, router just find the first rule which matches the request path's prefix;
    and if accuracy is True, it will find the rule which matches the whole path.

    Attention:
        Do NOT let one rule to be another's prefix. Or may get some result unexpected. like this:

        @app.route("/index/name")

        @app.route("/index/<name>")

        They both match the request path: http://127.0.0.1/index/name

    """

    def __init__(self, accuracy=True):
        self.rules = dict()
        self.handler_args = dict()
        self.accuracy = accuracy

    def add_rule(self, path, methods, handler):
        """
        Add one rule-handler pair into the dict of rules. If one rule be added more than once,
        only the first time will be effective.
        :param path: route path.
        :param methods: request methods, should be a list.
        :param handler: request handler.
        :return: None
        """
        rule, args = self.__path_analysis(path)
        for method in methods:
            if (rule, method) not in self.rules:
                self.rules[(rule, method)] = handler
                if args:
                    self.handler_args[handler] = args

    def __path_analysis(self, path):
        seg_list = []
        args = []
        for seg in path.split("/"):
            m = re.match("<((?P<converter>\w+):)?(?P<arg_name>\w+)>", seg)
            if m:
                if m.group("converter"):
                    if "int" == m.group("converter"):
                        tmp = "(?P<%s>\d+)" % m.group("arg_name")
                    else:
                        tmp = "(?P<%s>\w+)" % m.group("arg_name")
                else:
                    tmp = "(?P<%s>\w+)" % m.group("arg_name")
                args.append((m.group("arg_name"), m.group("converter")))
            else:
                tmp = seg
            seg_list.append(tmp)
        pattern = "^" + "/".join(seg_list)
        if self.accuracy:
            pattern += "$"
        return pattern, args

    def get_handler(self, path, method):
        """
        Get the handler of this path and method.
        :param path: Request path.
        :param method: Request method, should be a string.
        :return: (handler, args). handler is the handler of this rule, args is handler's args.
        """
        for (rule, handler) in self.rules.items():
            if method != rule[1]:
                continue
            m = re.match(rule[0], path)
            args = dict()
            if m:
                if handler in self.handler_args:
                    for (arg, converter) in self.handler_args[handler]:
                        if converter == "int":
                            args[arg] = int(m.group(arg))
                        else:
                            args[arg] = str(m.group(arg))
                return handler, args
        return None, None
# -*- coding: utf-8 -*-
"""
    Url router for requests.
"""


class Rule(object):

    def __init__(self, path, methods):
        """create a Rule object.
        :param path: request path of this rule.
        :param methods: the request methods this rule supported.
        """
        assert(isinstance(path, str))
        assert(isinstance(methods, list))
        self.path = path
        self.methods = [method.upper() for method in methods]

    def is_method_supported(self, method):
        """Judge is method supported by this rule.
        :param method: request method
        :return: True if supported else False.
        """
        if method.upper() in self.methods:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.path, str(self.methods)))

    def __eq__(self, other):
        return (self.path, self.methods) == (other.path, other.methods)


class Router(object):

    def __init__(self):
        self.rules = dict()

    def add_rule(self, path, methods, func):
        """
        Add one rule-handler pair into the dict of rules. If one rule be added more than once,
        only the first time will be effective.
        :param path: route path.
        :param methods: request methods, should be a list.
        :param func: request handler.
        :return: None
        """
        rule = Rule(path, methods)
        if rule not in self.rules:
            self.rules[rule] = func

    def get_handler(self, path, method):
        """
        Get the handler of this path and method.
        :param path: Request path.
        :param method: Request method, should be a string.
        :return: Handler of this rule if exists else None.
        """
        for rule in self.rules:
            if path == rule.path and method in rule.methods:
                return self.rules[rule]
        return None
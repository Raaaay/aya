# -*- coding: utf-8 -*-
"""
    Url router for requests.
"""


class Router(object):

    def __init__(self):
        self.rules = dict()

    def add_rule(self, rule, func):
        if rule not in self.rules:
            self.rules[rule] = func

    def get_handler(self, rule):
        if rule in self.rules:
            return self.rules[rule]
        else:
            return None
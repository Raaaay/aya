# -*- coding: utf-8 -*-
from aya.router import Router


def test_rule():
    pass


def test_router():
    router = Router()
    router.add_rule("/index", ["GET", "PUT"], test_rule)
    func = router.get_handler("/index", "GET")
    assert(func == test_rule)
    func = router.get_handler("/index", "POST")
    assert(not func)


test_rule()
test_router()
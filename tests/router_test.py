# -*- coding: utf-8 -*-
from aya.router import Rule
from aya.router import Router


def test_rule():
    r1 = Rule("/index", ["GET"])
    r2 = Rule("/index", ["POST"])
    r3 = Rule("/index", ["GET"])
    assert(r1 == r3)
    assert(r1 != r2)
    assert(r3 in [r1, r2])


def test_router():
    r1 = Rule("/index", ["GET"])
    r2 = Rule("/index", ["POST"])
    router = Router()
    router.add_rule("/index", ["GET", "PUT"], test_rule)
    func = router.get_handler("/index", "GET")
    assert(func == test_rule)
    func = router.get_handler("/index", "POST")
    assert(not func)


test_rule()
test_router()
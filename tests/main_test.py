# -*- coding: utf-8 -*-
from aya.app import Aya

app = Aya()


@app.route("/index", method=["GET", "POST"])
def say_hello():
    print "hello, aya."


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
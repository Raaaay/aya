# -*- coding: utf-8 -*-
from aya.app import Aya

app = Aya()


@app.route("/", methods=["GET", "POST"])
def say_hello():
    return 200


@app.route("/<string:name>/<int:age>/profile")
def my_profile(name, age):
    app.set_cookie("hello", "world")
    app.set_response_cookie_info(path="/", domain="127.0.0.1")
    return "my name is %s, and my age is %d, this is my profile." % (name, age)

if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
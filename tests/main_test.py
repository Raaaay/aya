# -*- coding: utf-8 -*-
from aya.app import Aya

app = Aya()


@app.route("/index", methods=["GET", "POST"])
def say_hello():
    return 200


@app.route("/aya", methods=["GET"])
def say_hi():
    return 200, "Aya"


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
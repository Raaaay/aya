README
----------
Aya是一个简单的纯python开发的web框架，遵循[WSGI](http://wsgi.readthedocs.org/en/latest/)协议标准[PEP3333](https://www.python.org/dev/peps/pep-3333/)。


它的使用方法非常简单，在引入了Aya包之后，一个简单的示例如下：


    # -*- coding: utf-8 -*-
    from aya.app import Aya
    
    app = Aya()
    
    
    @app.route("/", methods=["GET", "POST"])
    def say_hello():
        return 200, "hello"
    
    
    @app.route("/<string:name>/<int:age>")
    def my_profile(name, age):
        return "my name is %s, and I am %d this year." % (name, age)
    
    if __name__ == "__main__":
        app.run("127.0.0.1", 8080)


**注意：**


所有的静态资源的Request Path都必须以*static*开头，如*http://127.0.0.1/static/test.jpg*，可以通过


    app.set_static_root(your_root_path)
来指定静态文件文件夹路径。
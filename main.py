from flask import Flask, render_template, \
    request, make_response, redirect

from orm import model

import datetime

from orm import ormmanage as manage

app = Flask(__name__)


@app.route('/')
def index():
    user = None
    user = request.cookies.get("name")

    if user:
        print("之前已经登录")
    else:
        print("之前没有登录")

    return render_template("index.html", userinfo=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)

        # return render_template("lists.html",lists=[1,2,3,4,5])
        # return redirect("/lists")

        # 为了让响应可以携带头信息，需要构造响应

        result = manage.checkUser(username, password)
        res = make_response(redirect("/lists"))
        res.set_cookie('name', result.username,
                       expires=datetime.datetime.now() + datetime.timedelta(days=7))
        ids = str(result.id)
        res.set_cookie('userid', ids,
                       expires=datetime.datetime.now() + datetime.timedelta(days=7))
        return res


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)

        manage.insertUser(username, password)

        return render_template("login.html")


#书籍列表

@app.route("/lists")
def lists():
    userid = request.cookies.get("userid")
    result = manage.checkBook(userid)
    user = request.cookies.get("id")
    return render_template("lists.html", infoarry=result, name=user)


# 创建书籍
@app.route("/insertbook", methods=["GET", "POST"])
def insertbook():
    if request.method == "GET":
        return render_template("insertbook.html")
    elif request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        price = int(price)
        desc = request.form["desc"]
        userid = request.cookies.get("userid")
        userid = int(userid)
        print(name, price, desc, userid)
        result = manage.insertBook(name, price, desc, userid)
        return redirect("/lists")


# 删除书籍
@app.route("/deletebook/<int:id>")
def deletebook(id):
    print("----------------------", id)
    manage.deleteBook(id)
    return redirect("/lists")


# 修改书籍
@app.route("/updatebook/<int:id>", methods=["GET", "POST"])
def updatebook(id):
    if request.method == "GET":
        result = manage.checkBook(id)
        return render_template("updatebook.html", result=result, id=id)
    elif request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        desc = request.form["desc"]
        print("################################################")
        print(name, price, desc)
        result = manage.updateBook(id, name, price, desc)
        return redirect("/lists")


# 书籍详情
@app.route("/detail/<int:id>")
def detail(id):
    user = None
    user = request.cookies.get("name")
    result = manage.checkBook(id)
    return render_template("detail.html", infoarry=result, id=id)


# 退出
@app.route("/quit")
def quit():
    res = make_response(redirect("/"))
    res.delete_cookie("name")
    return res


if __name__ == '__main__':
    app.run(debug=True)

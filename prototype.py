from pickle import TRUE
from typing import final
from urllib import request
from flask import Flask, render_template, request, session
import sqlite3

app = Flask("__FoodOrderSystem__", template_folder="templates", static_folder="static")
app.secret_key = "Dgjoewheighe"
conn = sqlite3.connect("foodsystem.db")
db = "foodsystem.db"


@app.route("/")
def index():
    return render_template("index.html", title="Food Order System")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn
        print("Opened database successfully")
        try:
            print("trying")
            newUser = request.form["new-username"]
            newPwd = request.form["new-pwd"]
            fname = request.form["fname"]
            lname = request.form["lname"]

            with sqlite3.connect(db) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Users (UserName,FirstName,LastName,Password) VALUES(?,?,?,?)", (newUser,fname,lname,newPwd))
                con.commit()
                print("succ")
                msg = "Account created successfully"
        except:
            con.rollback()
            print("bad")
            msg = "Creation failed, try again"
        finally:
            return render_template("login.html", msg = msg)

    if request.method =="GET":
        return render_template("login.html")

@app.route("/createaccount", methods=["GET","POST"])
def createaccount():
    return render_template("signup.html")
    

@app.route("/retail/options", methods=["GET","POST"])
def options():
    if request.method == "POST":
        session["login"] = request.form
        login = session["login"]
        username = login["username"]
        return render_template("retail.html", username = username)
    elif request.method =="GET":
        login = session["login"]
        username = login["username"]
        return render_template("retail.html", username = username)

@app.route("/retail/createorder")
def createorder():
    return render_template("neworder.html")

@app.route("/user/pastorders")
def viewpastorders():
    return render_template("viewporders.html")

@app.route("/staff")
def staffoptions():
    return render_template("staff.html")

@app.route("/staff/allorders")
def revieworders():
    return render_template("staffAll.html")

@app.route("/retail/cart")
def checkout():
    return render_template("cart.html")

app.run(host="0.0.0.0", port=81)
from pickle import TRUE
from typing import final
from urllib import request
from flask import Flask, render_template, request, session, redirect
import sqlite3
from datetime import date

app = Flask("__FoodOrderSystem__", template_folder="templates", static_folder="static")
app.secret_key = "Dgjoewheighe"
db = "foodsystem.db"
conn = sqlite3.connect(db)

def fetchQuery(query):
    sqlite3.connect(db).row_factory = sqlite3.Row
    cur=sqlite3.connect(db).cursor()
    cur.execute(query)
    result = cur.fetchall()
    return result

def commitQuery(query):
    con = sqlite3.connect(db)
    print("connected")
    cur = con.cursor()
    print("cursor")
    cur.execute(query)
    print("Query executed")
    con.commit()
    print("committed")

# route for index.hmtl, will immediately redirect to login page
@app.route("/")
def index():
    return render_template("index.html")

#login page, POST from creating an account in the account page.
@app.route("/login", methods=["GET","POST"])
def login():
    #POST from account page
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
                cur.execute("INSERT INTO Users (UserName,FirstName,LastName,Password,UserType) VALUES(?,?,?,?,?)", (newUser,fname,lname,newPwd,"retail"))
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
        session.clear()
        return render_template("login.html")

@app.route("/createaccount", methods=["GET","POST"])
def createaccount():
    return render_template("signup.html")
    
@app.route("/validate", methods=["GET", "POST"])
def validate():
    if request.method == "POST":
        conn
        session["login"] = request.form
        login = session["login"]
        username = login["username"]
        pwd = login["pwd"]
        userlogin = (username, pwd)
        type=0
        try:
            with sqlite3.connect(db) as con:
                cur=con.cursor()
                cur.execute("SELECT UserName, Password FROM Users")
                userlist = cur.fetchall()
                if userlogin in userlist:
                    print("user in login list")
                    cur.execute(f"SELECT UserType FROM Users WHERE UserName = '{username}'")
                    type = cur.fetchall()
                    confirm=True
                        
                else:
                    print("user not in list")
                    confirm=False
        except:
            print("process aborted")
            confirm = False
        finally:
            username = login["username"]
            confirm=confirm
    elif request.method == "GET":
        confirm = False
    print(confirm)
    return render_template("loginvalidation.html", username=username, confirm=confirm, type=type, retail=([('retail',)]), staff=([('staff',)]))

@app.route("/joey", methods=["GET","POST"])
def foodcreation():
    msg=""
    if request.method == "POST":
        try:
            foodname = request.form["foodname"]
            descr = request.form["description"]
            itemprice = request.form["price"]
            category = request.form["category"]
            with sqlite3.connect(db) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Items (ItemName,ItemDescription,ItemPrice,Category) VALUES(?,?,?,?)", (foodname, descr, itemprice, category))
                con.commit()
                msg = "item created"
        except:
            print("exception")
            msg = "try again"
    return render_template("foodcreation.html", msg=msg)


@app.route("/retail/options", methods=["GET","POST"])
def options():
    username = session["login"]["username"]
    orderlist=[]
    try:
        with sqlite3.connect(db) as con:
            userID = fetchQuery(f"SELECT UserID FROM Users WHERE Username = '{username}'")
            print(userID)
            orderlist = fetchQuery(f"SELECT * FROM Orders WHERE UserID = '{userID[0][0]}'")
            print(orderlist)
    except:
        print("exception")
    return render_template("retail.html", username = username, orderlist=orderlist, count=0)

@app.route("/orders/<OrderID>")
def vieworder(OrderID):
    try:
        orderitems = fetchQuery(f"SELECT OrderItems.ItemID, Items.ItemName, ItemQuantity, Items.ItemPrice FROM OrderItems INNER JOIN Items on items.ItemID = OrderItems.ItemID WHERE OrderID = {OrderID}")
        print(orderitems)
        orderlists = []
        count = 0
        for item in orderitems:
            orderlist = list(orderitems[count])
            orderlist[3] = orderlist[3]*orderlist[2]
            orderlists.append(orderlist)
            count +=1
        orderitems = tuple(orderlists)
        print(orderitems)
        orderprice = fetchQuery(f"SELECT TotalPrice FROM Orders WHERE OrderID = {OrderID}")
    except:
        orderprice=0
        orderitems=0
        print("exception")
    return render_template("vieworder.html", orderprice=orderprice[0][0], orderitems=orderitems, username = session["login"]["username"], OrderID = OrderID)

@app.route("/retail/createorder")
def createorder():
    return render_template("neworder.html")

@app.route("/user/pastorders")
def viewpastorders():
    return render_template("viewporders.html")

@app.route("/staff")
def staffoptions():
    today = date.today().strftime("%d/%m")
    try:
        with sqlite3.connect(db) as con:
            orderlist = fetchQuery(f"SELECT Orders.*, Users.FirstName, Users.LastName FROM Orders INNER JOIN Users ON Orders.UserID = Users.UserID WHERE Date = '{today}'")
    except:
        orderlist=[]
        print("exception")
    return render_template("staff.html", username = session["login"]["username"], orderlist = orderlist, today=today)

@app.route("/staff/allorders")
def revieworders():
    try:
        with sqlite3.connect(db) as con:
            orderlist = fetchQuery(f"SELECT Orders.*, Users.FirstName, Users.LastName FROM Orders INNER JOIN Users ON Orders.UserID = Users.UserID")
    except:
        orderlist=[]
        print("exception")
    return render_template("staffAll.html", username = session["login"]["username"], orderlist = orderlist)

@app.route("/retail/cart")
def checkout():
    return render_template("cart.html")

app.run(host="0.0.0.0", port=81)
from flask import Flask, render_template

app = Flask("__FoodOrderSystem__", template_folder="templates", static_folder="static")
@app.route("/")
def index():
    return render_template("index.html", title="Food Order System")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/retail/options")
def options():
    return render_template("retail.html")

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
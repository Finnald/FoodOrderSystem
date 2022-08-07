from flask import Flask
from flask import render_template

app = Flask("__FoodOrderSystem__")
@app.route("/")
def index():
    name = "Joey"
    return render_template("Home.html", title="Food Order System", username=name )

@app.route("/login")
def login():
    return render_template("Login.html")

@app.route("/user/options")
def options():
    return render_template("User.html")

@app.route("/user/createorder")
def createorder():
    return render_template("User-Create-Order.html")

@app.route("/user/pastorders")
def viewpastorders():
    return render_template("viewporders.html")

@app.route("/user/staff/options")
def staffoptions():
    return render_template("staffpage.html")

@app.route("/user/staff/revieworders")
def revieworders():
    return render_template("review.html")

@app.route("/user/order/checkout")
def checkout():
    return render_template("Checkout.html")

app.run(host="0.0.0.0", port=81)
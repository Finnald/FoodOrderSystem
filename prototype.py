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
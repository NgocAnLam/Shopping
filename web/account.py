from utils.database import connectDB
from web.utils import generate_customer_code
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import Blueprint, request, session, render_template, redirect, url_for

web_account_bp = Blueprint('web_account', __name__)

db = connectDB()
accountDB = db["Account"]


@web_account_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        createTime = datetime.now()
        email = request.form["email"]
        username = request.form["username"]
        phone = request.form["phone"]
        province = request.form["province"]
        district = request.form["district"]
        ward = request.form["ward"]
        street = request.form["street"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        hashed_password = generate_password_hash(password, method="sha256")

        if password != confirm:
            return render_template(
                "web/signup.html", error_message="Mật khẩu không trùng nhau"
            )

        if accountDB.find_one({"email": email}):
            return render_template(
                "web/signup.html", error_message="Tài khoản đã tồn tại"
            )

        accountDB.insert_one(
            {
                "ID": generate_customer_code(username, phone, email, createTime),
                "email": email,
                "username": username,
                "password": hashed_password,
                "phone": phone,
                "address": street + ", " + ward + ", " + district + ", " + province,
                "shoppingCart": [],
                "orderProcessing": [],
                "orderTransit": [],
                "orderList": [],
                "commentList": [],
                "level": "Đồng",
                "createdTime": createTime,
                "loginTime": None,
            }
        )
        return redirect(url_for("web.web_account.login"))

    return render_template("web/signup.html")


@web_account_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = accountDB.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["userID"] = str(user["_id"])
            session["userName"] = user["username"]
            session["userEmail"] = user["email"]
            accountDB.update_one(
                {"_id": user["_id"]}, 
                {"$set": {"loginTime": datetime.now()}}
            )
            return redirect(url_for("web.web_home.home"))
        
        else:
            return render_template(
                "web/login.html", 
                error_message="username hoặc password không đúng"
            )

    return render_template("web/login.html")


@web_account_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("userID", None)
    session.pop("userName", None)
    session.pop("userEmail", None)
    return redirect(url_for("web.web_home.home"))


@web_account_bp.route("/info")
def info():
    isLogin = session.get("userName") is not None
    username = session.get("userName", "Tài khoản")
    email = session.get("userEmail")
    return {"isLogin": isLogin, "username": username, "email": email}


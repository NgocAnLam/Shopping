from utils.database import connectDB
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for

admin_account_bp = Blueprint('admin_account', __name__)

db = connectDB()
adminDB = db["Admin"]

@admin_account_bp.route("/signup", methods=["GET", "POST"])
def signupAdmin():
    if request.method == "GET":
        return render_template("admin/signup.html")

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        hashed_password = generate_password_hash(password, method="sha256")

        if password != confirm:
            return render_template("admin/signup.html", error_message="Mật khẩu không trùng nhau")

        if adminDB.find_one({"email": email}):
            return render_template("admin/signup.html", error_message="Tài khoản đã tồn tại")

        adminDB.insert_one({
            "email": email,
            "username": username,
            "password": hashed_password,
            "createdTime": datetime.now(),
            "loginTime": None,
        })

        return redirect(url_for("admin.loginAdmin"))


@admin_account_bp.route("/login", methods=["GET", "POST"])
def loginAdmin():
    if request.method == "GET":
        return render_template("admin/login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = adminDB.find_one({"username": username})

        if admin and check_password_hash(admin["password"], password):
            session["adminID"] = str(admin["_id"])
            session["adminName"] = admin["username"]
            session["adminEmail"] = admin["email"]

            adminDB.update_one(
                {"_id": admin["_id"]}, 
                {"$set": {"loginTime": datetime.now()}}
            )
            return redirect(url_for("admin.admin_dashboard.dashboardAdmin"))

        return render_template("admin/login.html", error_message="Invalid username or password")


@admin_account_bp.route("/logout", methods=["POST"])
def logoutAdmin():
    session.pop("adminID", None)
    session.pop("adminName", None)
    session.pop("adminEmail", None)
    return jsonify({"message": "logout successfully"})

from bson import ObjectId
from utils.database import connectDB
from flask import Blueprint, session, render_template

web_user_bp = Blueprint('web_user', __name__)

db = connectDB()
accountDB = db["Account"]


@web_user_bp.route("/user/<option>", methods=["GET"])
def user(option):
    userID = session.get("userID")

    sidebar = [
        ["Thông tin tài khoản", "account"],
        ["Đơn hàng đang xử lý", "processing"],
        ["Đơn hàng đang vận chuyển", "transit"],
        ["Đơn hàng đã giao", "confirmed"],
        ["Đánh giá sản phẩm", "review"],
    ]

    if option == "account":
        user = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})
        return render_template(
            "web/user.html", user=user, sideBar=sidebar, title="Thông tin tài khoản"
        )

    if option == "processing":
        user = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})
        return render_template(
            "web/user.html",
            orderList=user["orderProcessing"],
            sideBar=sidebar,
            title="Đơn hàng đang xử lý",
        )

    if option == "transit":
        user = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})
        return render_template(
            "web/user.html",
            orderList=user["orderTransit"],
            sideBar=sidebar,
            title="Đơn hàng đang vận chuyển",
        )

    if option == "confirmed":
        user = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})
        return render_template(
            "web/user.html",
            orderList=user["orderList"],
            sideBar=sidebar,
            title="Đơn hàng đã giao",
        )

    if option == "review":
        user = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})
        return render_template(
            "web/user.html", user=user, sideBar=sidebar, title="Đánh giá sản phẩm"
        )


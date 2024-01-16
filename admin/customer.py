from utils.database import connectDB
from flask import Blueprint, request, render_template

admin_customer_bp = Blueprint('admin_customer', __name__)

db = connectDB()
accountDB = db["Account"]

@admin_customer_bp.route("/", methods=["GET", "POST"])
def get_customer_list():
    id = request.args.get("id")
    option = request.args.get("option")

    if id == None and option == None:
        user = accountDB.find({}, {"_id": 0, "ID": 1, "email": 1, "username": 1, "phone": 1, "address": 1, "level": 1})
        return render_template("admin/customer.html", user=list(user), type="showAll")

    elif id != None and option == None:
        user = accountDB.find({"ID": id}, {"_id": 0})
        return render_template("admin/customer.html", user=list(user), type="info")

    else:
        if option == "process":
            user = accountDB.find({"ID": id}, {"_id": 0, "orderProcessing": 1})
            type = "process"
        elif option == "transit":
            user = accountDB.find({"ID": id}, {"_id": 0, "orderTransit": 1})
            type = "transit"
        elif option == "confirm":
            user = accountDB.find({"ID": id}, {"_id": 0, "orderList": 1})
            type = "confirm"
        else:
            user = accountDB.find({"ID": id}, {"_id": 0})
            type = "info"

        return render_template("admin/customer.html", user=list(user), type=type)
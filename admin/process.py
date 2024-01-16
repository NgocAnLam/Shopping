from datetime import datetime
from utils.database import connectDB
from flask import Blueprint, jsonify, render_template
from admin.utils import get_order_by_id

admin_process_bp = Blueprint('admin_process', __name__)

db = connectDB()
accountDB = db["Account"]

@admin_process_bp.route("/", methods=["GET"])
def getOrderProcess():
    userList = accountDB.find(
        {},
        {"_id": 0, "ID": 1, "email": 1, "address": 1, "phone": 1, "orderProcessing": 1},
    )
    order_list = [
        {
            "orderID": order["orderID"],
            "buyTime": order["buyTime"],
            "detail": order["detail"],
            "userID": user["ID"],
            "email": user["email"],
            "address": user["address"],
            "phone": user["phone"],
        }
        for user in userList
        for order in user["orderProcessing"]
    ]

    sorted_orders = sorted(order_list, key=lambda x: x["buyTime"])
    return render_template("admin/process.html", info=sorted_orders)


@admin_process_bp.route("/<customerID>/<orderID>", methods=["POST"])
def confirmOrderProcess(customerID, orderID):
    document_to_transfer = accountDB.find_one(
        {"ID": customerID, "orderProcessing.orderID": orderID},
        {"_id": 0, "email": 1, "orderProcessing": 1},
    )

    if document_to_transfer:
        target_order = get_order_by_id(document_to_transfer["orderProcessing"], orderID)

        accountDB.update_one(
            {"ID": customerID, "orderProcessing.orderID": orderID},
            {"$pull": {"orderProcessing": target_order}},
        )

        target_order["processedTime"] = datetime.now()

        accountDB.update_one(
            {"ID": customerID}, 
            {"$push": {"orderTransit": target_order}}, 
            upsert=True
        )

        return jsonify({"message": "Order added to the orderProcess successfully"})

    return jsonify({"message": "Order didn't add to the orderProcess successfully"})

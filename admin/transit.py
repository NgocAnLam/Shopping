from datetime import datetime
from utils.database import connectDB
from flask import Blueprint, jsonify, render_template
from admin.utils import get_order_by_id

admin_transit_bp = Blueprint('admin_transit', __name__)

db = connectDB()
accountDB = db["Account"]

@admin_transit_bp.route("/", methods=["GET"])
def getOrderTransit():
    userList = accountDB.find(
        {}, 
        {"_id": 0, "ID": 1, "email": 1, "address": 1, "phone": 1, "orderTransit": 1}
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
            "processedTime": order["processedTime"],
        }
        for user in userList
        for order in user["orderTransit"]
    ]

    sorted_orders = sorted(order_list, key=lambda x: x["processedTime"])
    return render_template("admin/transit.html", info=sorted_orders)

@admin_transit_bp.route("/<customerID>/<orderID>", methods=["POST"])
def confirmOrderTransit(customerID, orderID):
    document_to_transfer = accountDB.find_one(
        {"ID": customerID, "orderTransit.orderID": orderID},
        {"_id": 0, "email": 1, "orderTransit": 1},
    )

    if document_to_transfer:
        target_order = get_order_by_id(document_to_transfer["orderTransit"], orderID)

        accountDB.update_one(
            {"ID": customerID, "orderTransit.orderID": orderID},
            {"$pull": {"orderTransit": target_order}},
        )

        target_order["transitedTime"] = datetime.now()

        accountDB.update_one(
            {"ID": customerID}, 
            {"$push": {"orderList": target_order}}, 
            upsert=True
        )
        return jsonify({"message": "Order added to the orderTransit successfully"})

    return jsonify({"message": "Order did not add to the orderTransit successfully"})
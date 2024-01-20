import random
from bson import ObjectId
from utils.database import connectDB
from datetime import datetime
from flask import Blueprint, request, jsonify, session, render_template

web_shopping_cart_bp = Blueprint('web_shopping_cart', __name__)

db = connectDB()
accountDB = db['Account']
productDB = db["Product"]


@web_shopping_cart_bp.route("/shoppingCart", methods=["GET", "POST", "DELETE"])
def cart():
    userID = session.get("userID")

    if request.method == "GET":
        userCart = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})
        return render_template("web/shoppingCart.html", items=userCart["shoppingCart"])

    if request.method == "POST":
        data = request.get_json()
        productID, quantity = int(data.get("id")), int(data.get("quantity"))
        product = productDB.find_one({"id": productID}, {"_id": 0})
        if not product:
            return jsonify({"error": "Product not found"}), 404

        existItem = accountDB.find_one({"_id": ObjectId(userID), "shoppingCart.id": productID})

        if existItem:
            existProduct = next(
                (item for item in existItem["shoppingCart"] if item["id"] == productID),
                None,
            )
            newQuantity = existProduct["quantity"] + quantity

            if newQuantity == 0:
                accountDB.update_one(
                    {"_id": ObjectId(userID), "shoppingCart.id": productID},
                    {"$pull": {"shoppingCart": existProduct}},
                )
                return jsonify(
                    {"message": "Product removed from the cart successfully"}
                )

            else:
                queryAddItem = {
                    "id": existProduct["id"],
                    "name": existProduct["name"],
                    "brand": existProduct["brand"],
                    "orginalPrice": existProduct["orginalPrice"],
                    "price": existProduct["price"],
                    "quantity": newQuantity,
                    "total": newQuantity * existProduct["price"],
                    "image": existProduct["image"],
                    "url": existProduct["url"],
                    "timeAdd": datetime.now(),
                }

                accountDB.update_one(
                    {"_id": ObjectId(userID), "shoppingCart.id": productID},
                    {"$set": {"shoppingCart.$": queryAddItem}},
                )

                if quantity > 0:
                    return jsonify(
                        {"message": "Product added to the cart successfully"}
                    )

                return jsonify(
                    {"message": "Product removed from the cart successfully"}
                )

        else:
            queryAddItem = {
                "id": productID,
                "name": product["name"],
                "brand": product["brand_name"],
                "orginalPrice": product["original_price"],
                "price": product["price"],
                "quantity": quantity,
                "total": quantity * product["price"],
                "image": product["thumbnail_url"],
                "url": product["url_key"],
                "timeAdd": datetime.now(),
            }

            accountDB.update_one(
                {"_id": ObjectId(userID)}, {"$push": {"shoppingCart": queryAddItem}}
            )
            return jsonify({"message": "Product added to the cart successfully"}), 201

    if request.method == "DELETE":
        accountDB.update_one({"_id": ObjectId(userID)}, {"$set": {"shoppingCart": []}})
        return jsonify({"message": "All product removed from the cart successfully"})


@web_shopping_cart_bp.route("/infoCustomer")
def infoCustomer():
    userID = session.get("userID")
    userCart = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})
    if userCart:
        return jsonify({"user": userCart})
    else:
        return jsonify({"user": "Chưa đăng nhập"})


@web_shopping_cart_bp.route("/buyItems", methods=["GET", "POST"])
def buyItems():
    userID = session.get("userID")
    user = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})

    if request.method == "GET":
        return user["orderList"]

    if request.method == "POST":
        data = request.get_json()
        info = data.get("info")

        print(info)

        orderList = {
            "orderID": generate_order_id(),
            "buyTime": datetime.now(),
            "detail": [],
        }

        for item in info:
            productID = int(item.split(" - ")[-1])
            product = accountDB.find_one(
                {"shoppingCart.id": productID}, 
                {"_id": 0, "shoppingCart.$": 1}
            )
            product = product["shoppingCart"][0]

            orderList["detail"].append(
                {
                    "id": product["id"],
                    "name": product["name"],
                    "brand": product["brand"],
                    "price": product["price"],
                    "quantity": product["quantity"],
                    "total": product["total"],
                    "image": product["image"],
                    "url": product["url"],
                }
            )

            accountDB.update_one(
                {"_id": ObjectId(userID)},
                {"$pull": {"shoppingCart": {"id": product["id"]}}},
            )

        accountDB.update_one(
            {"_id": ObjectId(userID)}, 
            {"$push": {"orderProcessing": orderList}}
        )
        return jsonify(
            {"message": "Products added to the orderProcessing successfully"}
        )


def generate_order_id():
    order_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{'{:06}'.format(random.randint(0,999999))}"
    return order_id



@web_shopping_cart_bp.route("/processItems", methods=["GET", "POST"])
def processItems():
    userID = session.get("userID")
    user = accountDB.find_one({"_id": ObjectId(userID)}, {"_id": 0})

    if request.method == "GET":
        return user["orderList"]

    if request.method == "POST":
        data = request.get_json()
        info = data.get("info")
        return jsonify(
            {"message": "Products added to the orderProcessing successfully"}
        )
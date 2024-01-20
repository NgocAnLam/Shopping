import random
from utils.database import connectDB
from admin.utils import convert_to_slug
from flask import Blueprint, request, jsonify, render_template


admin_product_bp = Blueprint('adminProduct', __name__)

db = connectDB()
productDB = db["Product"]

@admin_product_bp.route("/", methods=["GET"])
def product():
    return render_template("admin/product.html")


@admin_product_bp.route("/add", methods=["GET", "POST"])
def addProduct():
    if request.method == "GET":
        return render_template("admin/product.html", type="add")

    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        brand_name = data.get("brand_name")
        price = int(data.get("price"))
        original_price = int(data.get("original_price"))
        thumbnail_url = data.get("thumbnail_url")
        category = int(data.get("category"))
        url_key = convert_to_slug(name) + "-p" + str(random.randint(1, 99999999))
        discount_rate = int(100 - (price / original_price * 100))
        id = random.randint(1, 99999999)

        data = {
            "id": id, "spid": id, "name": name, "url_key": url_key, "brand_name": brand_name,
            "price": price, "original_price": original_price, "discount": original_price - price,
            "discount_rate": discount_rate, "rating_average": 0,"review_count": 0, 
            "thumbnail_url": thumbnail_url, "quantity_sold": 0, "category": category
        }
        
        productDB.insert_one(data)
        return jsonify({"success": True})


@admin_product_bp.route("/remove", methods=["GET"])
def removeProduct():
    if request.method == "GET":
        return render_template("admin/product.html", type="remove")

    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        return jsonify({"name": name})


@admin_product_bp.route("/remove/getSuggestion", methods=["POST"])
def get_suggestion_remove():
    data = request.get_json()
    option = data.get("option", "")
    query = data.get("query", "")

    if query != "" and option == "id":
        num_less = int(query + ("0" * (9 - len(query))))
        num_greater = int(query + ("9" * (9 - len(query))))

        result = productDB.find(
            {option: {"$type": "int", "$gte": num_less, "$lte": num_greater}},
            {"_id": 0, option: 1},
        )
        return jsonify({"data": list(result), "query": query, "option": option})

    elif query != "" and option == "name":
        result = productDB.find({option: {"$regex": query, "$options": "i"}}, {"_id": 0, option: 1})
        return jsonify({"data": list(result), "query": query, "option": option})

    else:
        return jsonify({"data": [], "query": query, "option": option})


@admin_product_bp.route("/remove/getProduct", methods=["POST"])
def get_product_remove():
    data = request.get_json()
    option = data.get("option", "")
    query = data.get("dataProduct", "")

    if option == "id":
        query = int(query)

    result = productDB.find_one({option: query}, {"_id": 0})
    return jsonify({"data": result, "query": query, "option": option})


@admin_product_bp.route("/remove/removeProduct", methods=["POST"])
def remove_product():
    data = request.get_json()
    option = data.get("option", "")
    query = data.get("dataProduct", "")

    if option == "id":
        query = int(query)

    result = productDB.delete_one({option: query})

    if result.deleted_count == 1:
        return jsonify({"query": query, "option": option, "message": "Removed successfully"})

    return jsonify({"query": query, "option": option, "message": "Removed failed"})


@admin_product_bp.route("/update", methods=["GET"])
def updateProduct():
    if request.method == "GET":
        return render_template("admin/product.html", type="update")

    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        return jsonify({"name": name})


@admin_product_bp.route("/update/getSuggestion", methods=["POST"])
def get_suggestion_update():
    data = request.get_json()
    option = data.get("option", "")
    query = data.get("query", "")

    if query != "" and option == "id":
        num_less = int(query + ("0" * (9 - len(query))))
        num_greater = int(query + ("9" * (9 - len(query))))

        result = productDB.find(
            {option: {"$type": "int", "$gte": num_less, "$lte": num_greater}},
            {"_id": 0, option: 1},
        )

        return jsonify({"data": list(result), "query": query, "option": option})

    elif query != "" and option == "name":
        result = productDB.find(
            {option: {"$regex": query, "$options": "i"}}, 
            {"_id": 0, option: 1}
        )
        return jsonify({"data": list(result), "query": query, "option": option})

    else:
        return jsonify({"data": [], "query": query, "option": option})


@admin_product_bp.route("/update/getProduct", methods=["POST"])
def get_product_update():
    data = request.get_json()
    option = data.get("option", "")
    query = data.get("dataProduct", "")

    if option == "id":
        query = int(query)

    result = productDB.find_one({option: query}, {"_id": 0})
    return jsonify({"data": result, "query": query, "option": option})


@admin_product_bp.route("/update/updateProduct", methods=["POST"])
def update_product():
    data = request.get_json()
    info = data.get("info", "")
    id = data.get("id", "")
    productDB.update_one({"id": id}, {"$set": info})
    return jsonify({"info": info, "id": id})



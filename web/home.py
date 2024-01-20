from utils.database import connectDB
from flask import Blueprint, jsonify, render_template

web_home_bp = Blueprint('web_home', __name__)

db = connectDB()
categoryDB = db["Category"]
productDB = db["Product"]

@web_home_bp.route("/")
def home():
    resultQuantity = productDB.find({'category': 1789}, {'_id': 0, 'detail': 0}).sort('quantity_sold', -1).limit(6)
    resultDiscount = productDB.find({'category': 1789}, {'_id': 0, 'detail': 0}).sort('discount_rate', -1).limit(6)
    return render_template("web/home.html", data_quantity = list(resultQuantity), data_discount = list(resultDiscount))

@web_home_bp.route("/category")
def category():
    category = categoryDB.find({}, {"_id": 0, "text": 1, "name": 1, "code": 1, "icon_url": 1})
    return jsonify({"categoryList": list(category)})

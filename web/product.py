from datetime import datetime
from bson import ObjectId
from utils.database import connectDB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from web.shopping_cart import generate_order_id

web_product_bp = Blueprint('web_product', __name__)

db = connectDB()
productDB = db["Product"]
accountDB = db["Account"]

@web_product_bp.route("/<urlKeyProduct>", methods=["GET"])
def getProduct(urlKeyProduct):
    product = [productDB.find_one({"url_key": urlKeyProduct}, {"_id": 0})]

    try:
        detail = product[0]["detail"][0]
    except:
        detail = None

    return render_template("web/product.html", product = product[0], detail = detail)


@web_product_bp.route("/similar_product/<int:product_id>", methods=["GET", "POST"])
def getSimilarProduct(product_id):
    original = productDB.find_one({"id": product_id})
    productList = productDB.find({"category": original["category"]}, {"_id": 0})

    similar_products = [
        {
            "id": item["id"],
            "spid": item["spid"],
            "name": item["name"],
            "price": item["price"],
            "discountRate": item["discount_rate"],
            "urlKey": item["url_key"],
            "imgUrl": item["thumbnail_url"],
            "quantitySold": item["quantity_sold"],
            "rating": item["rating_average"],
        }
        for item in productList
        if 0.2 < calculate_similarity(original["name"], item["name"]) < 1
    ]

    sorted_list = sorted(similar_products, key=lambda x: x["name"])

    return sorted_list[:10] if len(sorted_list) > 6 else sorted_list

def calculate_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    similarity = cosine_similarity(vectorizer)
    return similarity[0, 1]


@web_product_bp.route('/buy_now/<int:product_id>/<int:quantity>', methods=['POST'])
def buy_now(product_id, quantity):
    userID = session.get("userID")

    product = productDB.find_one({'id': product_id})

    order = {
        "orderID": generate_order_id(),
        "buyTime": datetime.now(),
        "detail": [{
            "id": product_id,
            "name": product["name"],
            "brand": product["brand_name"],
            "price": product["price"],
            "quantity": quantity,
            "total": product["price"] * quantity,
            "image": product["thumbnail_url"],
            "url": product["url_key"],
        }]
    }
            
    accountDB.update_one(
        {"_id": ObjectId(userID)}, 
        {"$push": {"orderProcessing": order}}
    )
    
    return jsonify({'id': product_id, 'quantity': quantity})

@web_product_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = productDB.find_one({'id': product_id}, {'_id': 0, 'detail': 0})
    return product
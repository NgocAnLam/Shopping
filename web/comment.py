from datetime import datetime
from bson import ObjectId
from utils.database import connectDB
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

web_comment_bp = Blueprint('web_comment', __name__)

db = connectDB()
productDB = db["Product"]
commentDB = db["Comment"]
accountDB = db["Account"]


@web_comment_bp.route("/getComment/<int:product_id>")
def get_comment(product_id):        
    comment = (
        commentDB
        .find({"product_id": product_id}, {"_id": 0})
        .sort("time", -1)
        .limit(5)
    )
    return jsonify({"comments": list(comment)})


@web_comment_bp.route("/comment/<int:product_id>", methods=["GET", "POST"])
def comment(product_id):
    if request.method == "GET":
        userID = session.get("userID")
        product = productDB.find_one({'id': product_id}, {'_id': 0, 'detail': 0})
        user = accountDB.find_one({"_id": ObjectId(userID)}, {'_id': 0, 'email': 1, 'username': 1})
        return render_template("web/comment.html", product = product, user = user)
    
    if request.method == "POST":
        data = request.get_json()
        comment = data.get("comment")
        score = int(data.get("score"))
        email = session.get('userEmail')
        username = session.get('userName')

        commentDB.insert_one({
            "comment": comment,
            "score": score,
            "time": datetime.now(),
            "email": email, 
            "username": username, 
            "product_id": product_id,
        })

        product = productDB.find_one({"id": product_id})
        print(product)
        product['review_count'] += 1
        product['rating_average'] = round(product['rating_average'] * (product['review_count'] - 1) / product['review_count'], 1)

        productDB.update_one(
            {"id": product_id}, 
            {"$set": product}
        )

        return jsonify({"message": "Your comment added successfully"})
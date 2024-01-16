from utils.database import connectDB
from flask import Blueprint, jsonify, render_template

web_home_bp = Blueprint('web_home', __name__)

db = connectDB()
categoryDB = db["Category"]

@web_home_bp.route("/")
def home():
    return render_template("web/home.html")

@web_home_bp.route("/category")
def category():
    category = categoryDB.find({}, {"_id": 0, "text": 1, "name": 1, "code": 1, "icon_url": 1})
    return jsonify({"categoryList": list(category)})
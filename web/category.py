import math
from utils.database import connectDB
from web.utils import (
    checkCode, 
    getFilter, 
    getProductFromQuery, 
    createPaging,
    generate_substrings,
    calculate
)
from flask import Blueprint, request, jsonify, render_template

web_category_bp = Blueprint('web_category', __name__)

db = connectDB()
categoryDB = db["Category"]
productDB = db["Product"]


@web_category_bp.route("/<category>/<code>")
def showItems(category, code, numberItemsPerPage=24):
    if checkCode(category, code) == False:
        return render_template("web/404.html")

    query = getProductFromQuery(getFilter(code))

    if query is None:
        return render_template("web/404.html")
    items = list(productDB.find(query))
    try:
        page = int(request.args.get("page"))
    except:
        page = 1

    maxPage = math.ceil(len(items) / numberItemsPerPage)
    if page > maxPage:
        return render_template("web/404.html")

    list_items = [
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
        for item in list(items)[
            (page - 1) * numberItemsPerPage : (page) * numberItemsPerPage
        ]
    ]

    if len(list_items) == 0:
        return render_template("web/404.html")

    return render_template(
        "web/category.html",
        data=list_items,
        paging=createPaging(page, maxPage, len(items), numberItemsPerPage),
    )


@web_category_bp.route("/filter/<category>", methods=["GET"])
def filterCategory(category):
    filter = categoryDB.find({"name": category}, {"_id": 0, "filter": 1})
    filterList = list(filter)[0]["filter"]
    filterListChoose = []
    accessList = ["rating", "price", "brand"]
    for item in filterList:
        if item["query_name"] in accessList:
            filterListChoose.append(item)

    return jsonify(filterListChoose)


@web_category_bp.route("/search")
def search():
    q = request.args.get("q")
    originList = generate_substrings(q)
    origin = "|".join(originList)
    numberItemsPerPage = 24
    percentList = []
    itemsFiltered = []

    try:
        page = int(request.args.get("page"))
    except:
        page = 1

    items = list(productDB.find({"name": {"$regex": origin}}, {"_id": 0}))
    for text in items:
        originListLower = map(lambda a: a.lower(), originList)

        percent = calculate(originListLower, text["name"].lower(), len(originList))
        if percent > 0.1:
            itemsFiltered.append(text)
            percentList.append(percent)

    sorted_pairs = sorted(
        zip(itemsFiltered, percentList), key=lambda x: x[1], reverse=True
    )
    itemsSorted = [pair[0] for pair in sorted_pairs]

    maxPage = math.ceil(len(itemsSorted) / numberItemsPerPage)
    if page > maxPage:
        return render_template("web/404.html")

    list_items = [
        {
            "id": item["id"],
            "spid": item["spid"],
            "name": item["name"],
            "price": item["price"],
            "discountRate": item["discount_rate"],
            "urlKey": item["url_key"],
            "image": item["thumbnail_url"],
            "quantity": item["quantity_sold"],
            "rating": item["rating_average"],
        }
        for item in list(itemsSorted)[
            (page - 1) * numberItemsPerPage : (page) * numberItemsPerPage
        ]
    ]

    return render_template(
        "web/search.html",
        data=list_items,
        paging=createPaging(page, maxPage, len(itemsSorted), numberItemsPerPage),
        keyword=q,
        quantityKeyword=len(itemsSorted),
    )

from utils.database import connectDB
from admin.utils import get_a_week, get_a_month, get_a_year
from flask import Blueprint, request, jsonify, render_template

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

db = connectDB()
accountDB = db["Account"]
productDB = db["Product"]

@admin_dashboard_bp.route("/")
def dashboardAdmin():
    pipelineOrder = [
        {
            "$project": {
                "countProcessing": {"$size": "$orderProcessing"},
                "countTransit": {"$size": "$orderTransit"},
                "countList": {"$size": "$orderList"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "result": ["$countProcessing", "$countTransit", "$countList"],
            }
        },
    ]

    pipelineRevenue = [
        {"$unwind": "$orderList"},
        {
            "$project": {
                "_id": 0,
                "total_orderList": {"$sum": "$orderList.detail.total"},
            }
        },
    ]

    resultRevenue = list(accountDB.aggregate(pipelineRevenue))
    totalRevenue = sum(item["total_orderList"] for item in resultRevenue)

    resultOrder = list(accountDB.aggregate(pipelineOrder))
    countOrder = [sum(pair) for pair in zip(resultOrder[0]["result"], resultOrder[1]["result"])]

    return render_template(
        "admin/dashboard.html",
        totalProducts = productDB.count_documents({}),
        totalCustomers = accountDB.count_documents({}),
        totalProcessing = countOrder[0],
        totalTransit = countOrder[1],
        totalOrder = countOrder[2],
        totalRevenue = totalRevenue,
    )


@admin_dashboard_bp.route("/chartRevenue", methods=["POST"])
def chartRevenueDay():
    data = request.get_json()
    option = data.get("option", "")

    if option == "year":
        year = int(data.get("year", ""))
        dateList = get_a_year(year)
    elif option == "month":
        year = int(data.get("year", ""))
        month = int(data.get("month", ""))
        dateList = get_a_month(year, month)
    else:
        dateList = get_a_week()

    result = accountDB.find({}, {"_id": 0, "orderList": 1})

    for res in result:
        for i in res["orderList"]:
            for detail in i["detail"]:
                date = str(i["transitedTime"].date())
                if date in dateList.keys():
                    dateList[date] += detail["total"]

    dateList = dict(sorted(dateList.items()))

    return jsonify({
        "success": True,
        "key": list(dateList.keys()),
        "value": list(dateList.values()),
    })
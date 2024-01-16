import hashlib
import base64
from flask import request
from utils.database import connectDB


db = connectDB()
accountDB = db["Account"]
categoryDB = db["Category"]
productDB = db["Product"]
adminDB = db["Admin"]
commentDB = db["Comment"]


def generate_customer_code(username, phone, email, createTime):
    combined_info = f"{username}{phone}{email}{createTime}"
    hash_object = hashlib.sha512(combined_info.encode())
    hash_digest = hash_object.hexdigest()
    customer_code = base64.b64encode(hash_digest.encode())[:8].decode()
    return customer_code


def checkCode(category, code):
    isCode = categoryDB.find_one({"code": code, "name": category})
    if isCode:
        return True
    return False


def getFilter(code):
    filter = list(categoryDB.find({"code": code}, {"_id": 0, "filter": 1}))
    filterList = filter[0]["filter"]
    queryNameList = [i["query_name"] for i in filterList]
    accessList = ["brand", "price", "rating"]
    queryNameList = [item for item in queryNameList if item in accessList]
    filterDict = {
        key: request.args.get(key)
        for key in queryNameList
        if request.args.get(key) is not None
    }
    filterDict["category"] = int(code)
    return filterDict


def getProductFromQuery(filterList):
    try:
        if filterList["price"] != None and "," in filterList["price"]:
            price = filterList["price"].split(",")
            try:
                priceLow, priceHigh = map(int, price)
                if priceLow <= priceHigh:
                    filterList["price"] = {"$gte": priceLow, "$lte": priceHigh}
                else:
                    filterList["price"] = None
            except ValueError:
                filterList["price"] = None
    except:
        pass

    try:
        if filterList["rating"] != None:
            filterList["rating_average"] = int(filterList.pop("rating"))
            try:
                rating = round(float(filterList["rating_average"]), 1)
                if 0 <= rating <= 5:
                    filterList["rating_average"] = {"$gte": rating}
                else:
                    filterList["rating_average"] = None
            except ValueError:
                filterList["rating"] = None
    except:
        pass

    try:
        if filterList["brand"] != None:
            brand = filterList["brand"].split(",")
            filterList["brand"] = {"$in": brand}
            filterList["brand_name"] = filterList.pop("brand")
    except:
        pass

    return dict((key, value) for key, value in filterList.items() if value is not None)


def createPaging(page, maxPage, itemLength, numberItemsPerPage):
    pageDescription = []
    if maxPage <= 5:
        for i in range(1, maxPage + 1):
            pageDescription.append(i)
    elif page <= 3:
        pageDescription = [1, 2, 3, 4, 5, "...", maxPage]
    elif page >= maxPage - 2:
        pageDescription = [1, "...", maxPage - 4, maxPage - 3, maxPage - 2, maxPage - 1, maxPage]
    else:
        pageDescription = [ 1, "...", page - 2, page - 1, page, page + 1, page + 2, "...", maxPage]

    return {
        "current_page": page,
        "last_page": maxPage,
        "per_page": numberItemsPerPage,
        "total": itemLength,
        "description": pageDescription,
    }


def generate_substrings(originText):
    substrings = []
    words = originText.split()
    if len(words) > 1:
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                substring = " ".join(words[i:j])
                substrings.append(substring.lower())
                substrings.append(substring.upper())
                substrings.append(substring.capitalize())
    else:
        substrings.append(words[0].lower())
        substrings.append(words[0].upper())
        substrings.append(words[0].capitalize())

    substrings = set(substrings)
    return substrings


def calculate(originList, nameProduct, lenOriginList):
    score, wordSingle, wordMulti, wordOrigin = 0, 0, 0, 0

    for word in originList:
        wordOrigin += len(word)
        if (
            nameProduct.startswith(word + " ")
            or nameProduct.endswith(" " + word)
            or " " + word + " " in nameProduct
        ):
            wordSingle += len(word)
            wordMulti += 1
            continue

    score = round(((wordSingle / wordOrigin) * (wordMulti / lenOriginList)), 2)
    return score

import math
import re
from bson import ObjectId
from flask import Flask, request, jsonify, session, render_template, redirect,  url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import hashlib
import base64
from datetime import datetime
import random
import asyncio
import telegram
import configparser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from unidecode import unidecode

app = Flask(__name__)
app.secret_key = "your_secret_key"

client = MongoClient("mongodb://localhost:27017/")
db = client['NgocDungStore']
accountDB = db['Account']
categoryDB = db['Category']
productDB = db['Product']
adminDB = db['Admin']

# -- Read config file -----------------------------------------------------
def read_config(filename, section, key):
    config = configparser.ConfigParser()
    config.read(filename)
    if section in config and key in config[section]:
        return config[section][key]
    else:
        return None

token_telegram = read_config('info.ini', 'telegram', 'token')
id_telegram = read_config('info.ini', 'telegram', 'id')

# -- Bot Telegram ---------------------------------------------------------
async def send_test_message(token, id, message):
    try:
        telegram_notify = telegram.Bot(token)
        await telegram_notify.send_message(
            chat_id = id, 
            text = message, 
            parse_mode = 'Markdown')
    except Exception as ex:
        print(ex)

# asyncio.run(send_test_message(token, id, message))

# -- Admin ----------------------------------------------------------------
@app.route('/admin')
def admin():
    return render_template('admin/dashboard.html')

@app.route('/admin/signup', methods=['GET', 'POST'])
def signupAdmin():
    if request.method == 'GET':
        return render_template('admin/signup.html')
    
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        hashed_password = generate_password_hash(password, method='sha256')

        if password != confirm:
            return render_template('admin/signup.html', error_message='Mật khẩu không trùng nhau')

        if adminDB.find_one({'email': email}):
            return render_template('admin/signup.html', error_message='Username already exists')
        
        adminDB.insert_one({
            'email': email, 
            'username': username, 
            'password': hashed_password,
            'createdTime': datetime.now(),
            'loginTime': None,
            'orderList': []
        })

        return redirect(url_for('loginAdmin'))

@app.route('/admin/login', methods=['GET', 'POST'])
def loginAdmin():
    if request.method == 'GET':
        return render_template('admin/login.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = adminDB.find_one({'username': username})

        if admin and check_password_hash(admin['password'], password):
            session['adminID'] = str(admin['_id'])
            session['adminName'] = admin['username']
            session['adminEmail'] = admin['email']
            adminDB.update_one({'_id': admin['_id']}, {'$set': {'loginTime': datetime.now()}})
            return redirect(url_for('admin'))
        else:
            return render_template('admin/login.html', error_message='Invalid username or password')

@app.route('/admin/logout', methods=['POST'])
def logoutAdmin():
    session.pop('adminID', None)
    session.pop('adminName', None)
    session.pop('adminEmail', None)
    return jsonify({'success': True, 'message': 'logout successfully'})

@app.route('/admin/product', methods=['GET'])
def product():
    return render_template('admin/product.html')

@app.route('/admin/product/add', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'GET':
        return render_template('admin/product.html', type = 'add')
    
    if request.method == 'POST':
        data = request.get_json()

        name = data.get('name')
        brand_name = data.get('brand_name')
        price = int(data.get('price'))
        original_price = int(data.get('original_price'))
        thumbnail_url = data.get('thumbnail_url')
        category = int(data.get('category'))

        id = random.randint(1, 99999999)
        output_slug = convert_to_slug(name) + '-p' + str(id)

        info_product = {
            'id': id,
            'spid': id,
            'name': name,
            'url_key': output_slug,
            'brand_name': brand_name,
            'price': price,
            'original_price': original_price,
            'discount': original_price - price,
            'discount_rate': int(100 - (price / original_price * 100)),
            'rating_average': 0,
            'review_count': 0,
            'thumbnail_url': thumbnail_url,
            'quantity_sold': 0,
            'category': category
        }

        productDB.insert_one(info_product)
        return jsonify({'success': True})

def convert_to_slug(text):
    text = text.replace('/', ' ')
    text = text.replace(' - ', ' ')
    no_accents = unidecode(text)
    slug = no_accents.lower().replace(' ', '-')
    slug = ''.join(char if char.isalnum() or char == '-' else '' for char in slug)
    return slug

@app.route('/admin/product/remove', methods=['GET'])
def removeProduct():
    if request.method == 'GET':
        return render_template('admin/product.html', type = 'remove')
    
    if request.method == 'POST':
        data = request.get_json()

        name = data.get('name')
        return jsonify({'success': True, 'name': name})

@app.route('/admin/product/remove/getSuggestion', methods=['POST'])
def get_suggestion_remove():
    data = request.get_json()
    option = data.get('option', '')
    query = data.get('query', '')
    if query != '' and option == 'id':
        input_int1 = int(query + ('0' * (9 - len(query))))
        input_int2 = int(query + ('9' * (9 - len(query))))

        result = productDB.find(
            {
                option : {
                    "$type": "int",
                    "$gte": input_int1,
                    "$lte": input_int2
                }
            },
            {'_id': 0, option: 1}
        )
        return jsonify({
            'success': True, 
            'data': list(result), 
            'query': query, 
            'option': option
        })
    
    elif query != '' and option == 'name':
        result = productDB.find(
            {option: {"$regex": query, "$options": "i"}},
            {'_id': 0, option: 1}
        )
        return jsonify({
            'success': True, 
             'data': list(result), 
             'query': query, 
             'option': option
        })
    
    else:
        return jsonify({
            'success': True, 
            'data': [], 
            'query': query, 
            'option': option
        })


@app.route('/admin/product/remove/getProduct', methods=['POST'])
def get_product_remove():
    data = request.get_json()
    option = data.get('option', '')
    query = data.get('dataProduct', '')

    if option == 'id':
        query = int(query)

    result = productDB.find_one({option : query}, {'_id': 0})

    return jsonify({
        'success': True, 
        'data': result, 
        'query': query, 
        'option': option
    })

@app.route('/admin/product/remove/removeProduct', methods=['POST'])
def remove_product():
    data = request.get_json()
    option = data.get('option', '')
    query = data.get('dataProduct', '')

    if option == 'id':
        query = int(query)

    result = productDB.delete_one({option: query})

    if result.deleted_count == 1:
        return jsonify({
            'success': True, 
            'query': query, 
            'option': option,
            'message': 'Removed successfully'
        })
    else:
        return jsonify({
            'success': False, 
            'query': query, 
            'option': option,
            'message': 'Removed failed'
        })


@app.route('/admin/product/update', methods=['GET'])
def updateProduct():
    if request.method == 'GET':
        return render_template('admin/product.html', type = 'update')
    
    if request.method == 'POST':
        data = request.get_json()

        name = data.get('name')
        return jsonify({'success': True, 'name': name})

@app.route('/admin/product/update/getSuggestion', methods=['POST'])
def get_suggestion_update():
    data = request.get_json()
    option = data.get('option', '')
    query = data.get('query', '')
    if query != '' and option == 'id':
        input_int1 = int(query + ('0' * (9 - len(query))))
        input_int2 = int(query + ('9' * (9 - len(query))))

        result = productDB.find(
            {
                option : {
                    "$type": "int",
                    "$gte": input_int1,
                    "$lte": input_int2
                }
            },
            {'_id': 0, option: 1}
        )
        return jsonify({
            'success': True, 
            'data': list(result), 
            'query': query, 
            'option': option
        })
    
    elif query != '' and option == 'name':
        result = productDB.find(
            {option: {"$regex": query, "$options": "i"}},
            {'_id': 0, option: 1}
        )
        return jsonify({
            'success': True, 
             'data': list(result), 
             'query': query, 
             'option': option
        })
    
    else:
        return jsonify({
            'success': True, 
            'data': [], 
            'query': query, 
            'option': option
        })


@app.route('/admin/product/update/getProduct', methods=['POST'])
def get_product_update():
    data = request.get_json()
    option = data.get('option', '')
    query = data.get('dataProduct', '')

    if option == 'id':
        query = int(query)

    result = productDB.find_one({option : query}, {'_id': 0})

    return jsonify({
        'success': True, 
        'data': result, 
        'query': query, 
        'option': option
    })

@app.route('/admin/product/update/updateProduct', methods=['POST'])
def update_product():
    data = request.get_json()
    info = data.get('info', '')
    id = data.get('id', '')

    result = productDB.update_one(
        {'id': id}, 
        {"$set": info}
    )
    
    return jsonify({'info': info,  'id': id})



@app.route('/admin/customer', methods=['GET','POST'])
def getCustomerList():
    id = request.args.get('id')
    option = request.args.get('option')

    if id == None and option == None:
        user = accountDB.find(
            {}, 
            {'_id':0, 'ID': 1, 'email': 1, 'username': 1, 'phone': 1, 'address': 1, 'level': 1}
        )
        return render_template('admin/customer.html', user = list(user), type = 'showAll')
    
    elif id != None and option == None:
        option = "info"
        user = accountDB.find({'ID': id}, {'_id':0})
        return render_template('admin/customer.html', user = list(user), type = 'info')
    else:
        if option == "process":
            user = accountDB.find({'ID': id}, {'_id':0, 'orderProcessing': 1})
            return render_template('admin/customer.html', user = list(user), type = 'process')
        elif option == "transit":
            user = accountDB.find({'ID': id}, {'_id':0, 'orderTransit': 1})
            return render_template('admin/customer.html', user = list(user), type = 'transit')
        elif option == "confirm":
            user = accountDB.find({'ID': id}, {'_id':0, 'orderList': 1})
            return render_template('admin/customer.html', user = list(user), type = 'confirm')
        else:
            user = accountDB.find({'ID': id}, {'_id':0})
            return render_template('admin/customer.html', user = list(user), type = 'info')

@app.route('/admin/process', methods=['GET'])
def getOrderProcess():
    user = accountDB.find({}, {'_id': 0, 'ID': 1, 'email': 1, 'address': 1, 'phone': 1, 'orderProcessing': 1})

    order_list = []
    for user in user:
        for order in user['orderProcessing']:
            order_list.append({
                'orderID': order['orderID'],
                'buyTime': order['buyTime'],
                'detail': order['detail'], 
                'userID': user['ID'],
                'email': user['email'], 
                'address': user['address'], 
                'phone': user['phone'],
            })

    sorted_orders = sorted(order_list, key=lambda x: x['buyTime'])
    return render_template('admin/process.html', info = sorted_orders)

@app.route('/admin/transit', methods=['GET'])
def getOrderTransit():
    user = accountDB.find({}, {'_id': 0, 'ID': 1, 'email': 1, 'address': 1, 'phone': 1, 'orderTransit': 1})

    order_list = []
    for user in user:
        for order in user['orderTransit']:
            order_list.append({
                'orderID': order['orderID'],
                'buyTime': order['buyTime'],
                'detail': order['detail'], 
                'userID': user['ID'],
                'email': user['email'], 
                'address': user['address'], 
                'phone': user['phone'],
                'processedTime': order['processedTime'],
            })
    sorted_orders = sorted(order_list, key=lambda x: x['processedTime'])
    return render_template('admin/transit.html', info = sorted_orders)

@app.route('/admin/order/process/<customerID>/<orderID>', methods=['POST'])
def confirmOrderProcess(customerID, orderID):
    document_to_transfer = accountDB.find_one(
        {"ID": customerID,"orderProcessing.orderID": orderID},
        {'_id': 0, 'email': 1,'orderProcessing': 1}
    )

    if document_to_transfer:
        target_order = get_order_by_id(document_to_transfer['orderProcessing'], orderID)
        accountDB.update_one(
            {"ID": customerID, "orderProcessing.orderID": orderID}, 
            {"$pull": {"orderProcessing": target_order}}
        )

        target_order['processedTime'] = datetime.now()
        accountDB.update_one(
            {"ID": customerID}, 
            {"$push": {"orderTransit": target_order}}, upsert=True
        )

        message = f"Mã khách hàng ({customerID} - {document_to_transfer['email']}) có đơn hàng ({orderID}) đang vận chuyển."
        asyncio.run(send_test_message(token_telegram, id_telegram, message))

        return jsonify({'success': True, 'message': 'Order added to the orderProcess successfully', 'user': target_order})
    else:
        return jsonify({'success': False, 'message': 'Order did not add to the orderProcess successfully'})
    
@app.route('/admin/order/transit/<customerID>/<orderID>', methods=['POST'])
def confirmOrderTransit(customerID, orderID):
    document_to_transfer = accountDB.find_one(
        {"ID": customerID, "orderTransit.orderID": orderID},
        {'_id': 0, 'email': 1,'orderTransit': 1}
    )

    if document_to_transfer:
        target_order = get_order_by_id(document_to_transfer['orderTransit'], orderID)
        accountDB.update_one(
            {"ID": customerID, "orderTransit.orderID": orderID}, 
            {"$pull": {"orderTransit": target_order}}
        )

        target_order['transitedTime'] = datetime.now()
        accountDB.update_one(
            {"ID": customerID}, 
            {"$push": {"orderList": target_order}}, upsert=True
        )

        message = f"Mã khách hàng ({customerID} - {document_to_transfer['email']}) có đơn hàng ({orderID}) đã giao thành công."
        asyncio.run(send_test_message(token_telegram, id_telegram, message))

        return jsonify({'success': True, 'message': 'Order added to the orderTransit successfully', 'user': target_order})
    else:
        return jsonify({'success': False, 'message': 'Order did not add to the orderTransit successfully'})

def get_order_by_id(order_list, target_order_id):
    for order in order_list:
        if order.get('orderID') == target_order_id:
            return order
    return None



# -- Account ----------------------------------------------------------------
@app.route('/')
def home():
    return render_template('web/home.html')

def generate_customer_code(username, phone, email, createTime):
    combined_info = f"{username}{phone}{email}{createTime}"
    hash_object = hashlib.sha512(combined_info.encode())
    hash_digest = hash_object.hexdigest()
    customer_code = base64.b64encode(hash_digest.encode())[:8].decode()
    return customer_code

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        province = request.form['province']
        district = request.form['district']
        ward = request.form['ward']
        street = request.form['street']
        password = request.form['password']
        confirm = request.form['confirm']
        hashed_password = generate_password_hash(password, method='sha256')

        if password != confirm:
            return render_template(
                'signup.html', 
                error_message='Mật khẩu không trùng nhau'
            )

        if accountDB.find_one({'email': email}):
            return render_template(
                'signup.html', 
                error_message='Username already exists'
            )
        
        createTime = datetime.now()

        user = {
            'ID': generate_customer_code(username, phone, email, createTime),
            'email': email, 
            'username': username, 
            'password': hashed_password,
            'phone': phone,
            'address': street + ', ' + ward + ', ' + district + ', ' + province,
            'shoppingCart': [],
            'orderProcessing': [],
            'orderTransit': [],
            'orderList': [],
            'reviewList': [],
            'level': 'Đồng',
            'createdTime': createTime,
            'loginTime': None,
        }

        accountDB.insert_one(user)
        return redirect(url_for('login'))

    return render_template('web/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = accountDB.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            session['userID'] = str(user['_id'])
            session['userName'] = user['username']
            session['userEmail'] = user['email']
            accountDB.update_one({'_id': user['_id']}, {'$set': {'loginTime': datetime.now()}})
            return redirect(url_for('home'))
        else:
            return render_template('web/login.html', error_message='Invalid username or password')
        
    return render_template('web/login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('userID', None)
    session.pop('userName', None)
    session.pop('userEmail', None)
    return redirect(url_for('home'))

# Initial
@app.route('/info')
def info():
    isLogin = session.get('userName') is not None
    username = session.get('userName', 'Tài khoản')
    email = session.get('userEmail')
    return {'isLogin': isLogin, 'username': username, 'email': email}

@app.route('/category')
def category():
    categoryList = list(categoryDB.find({}, {'_id': 0, 'text': 1, 'name': 1, 'code': 1, 'icon_url': 1}))
    return jsonify({'categoryList': categoryList})

@app.route('/<category>/<code>')
def showItems(category, code, numberItemsPerPage = 24):
    if checkCode(category, code) == False:
        return render_template('web/404.html')
    
    query = getProductFromQuery(getFilter(code))
    if query is None:
        return render_template('web/404.html')
    items = list(productDB.find(query))
    try:
        page = int(request.args.get('page'))
    except:
        page = 1

    maxPage = math.ceil(len(items) / numberItemsPerPage)
    if page > maxPage:
        return render_template('web/404.html')
    
    list_items = [{
        'id': item['id'],
        'spid': item['spid'],
        'name': item['name'], 
        'price': item['price'], 
        'discountRate': item['discount_rate'], 
        'urlKey': item['url_key'], 
        'imgUrl': item['thumbnail_url'], 
        'quantitySold': item['quantity_sold'],
        'rating': item['rating_average'], 
    } for item in list(items)[(page - 1) * numberItemsPerPage : (page) * numberItemsPerPage]]

    if len(list_items) == 0:
        return render_template('web/404.html')
    
    return render_template(
        'web/category.html', 
        data = list_items, 
        paging = createPaging(page, maxPage, len(items), numberItemsPerPage)
    )

def checkCode(category, code):
    isCode = categoryDB.find_one({'code': code, 'name': category}) 
    if isCode:
        return True
    return False

def getFilter(code):
    filter = list(categoryDB.find({'code': code}, {'_id': 0, 'filter': 1}))
    filterList = filter[0]['filter']
    queryNameList = [i['query_name'] for i in filterList]
    accessList = ['brand', 'price', 'rating']
    queryNameList = [item for item in queryNameList if item in accessList]
    filterDict = {key: request.args.get(key) for key in queryNameList if request.args.get(key) is not None}
    filterDict['category'] = int(code)
    return filterDict

def getProductFromQuery(filterList):
    try:
        if filterList['price'] != None and ',' in filterList['price']:
            price = filterList['price'].split(',')
            try:
                priceLow, priceHigh = map(int, price)
                if priceLow <= priceHigh:
                    filterList['price'] = {'$gte': priceLow, '$lte': priceHigh}
                else:
                    filterList['price'] = None
            except ValueError:
                filterList['price'] = None
    except:
        pass

    try:     
        if filterList['rating'] != None:
            filterList['rating_average'] = int(filterList.pop('rating'))
            try:
                rating = round(float(filterList['rating_average']), 1)
                if 0 <= rating <= 5:
                    filterList['rating_average'] = {'$gte': rating}
                else:
                    filterList['rating_average'] = None
            except ValueError:
                filterList['rating'] = None
    except:
        pass

    try:
        if filterList['brand'] != None:
            brand = filterList['brand'].split(',')
            filterList['brand'] = {"$in": brand}
            filterList['brand_name'] = filterList.pop('brand')
    except:
        pass

    return dict((key, value) for key, value in filterList.items() if value is not None)

def createPaging(page, maxPage, itemLength, numberItemsPerPage):
    pageDescription = []
    if (maxPage <= 5):
        for i in range(1, maxPage + 1):
            pageDescription.append(i)
    elif (page <= 3):
        pageDescription = [1, 2, 3, 4, 5, "...", maxPage]
    elif (page >= maxPage - 2):
        pageDescription = [1, "...", maxPage-4, maxPage-3, maxPage-2, maxPage-1, maxPage]
    else:
        pageDescription = [1 , "...", page - 2, page - 1, page, page + 1, page + 2, "...", maxPage]


    paging = {
        'current_page': page,
        'last_page': maxPage, 
        'per_page': numberItemsPerPage,
        'total': itemLength,
        'description': pageDescription
    }
    print(paging)
    return paging

@app.route('/filter/<category>', methods=['GET'])
def filterCategory(category):
    filter = categoryDB.find({'name': category},{'_id': 0, 'filter': 1})
    filterList = list(filter)[0]['filter']
    filterListChoose = []
    accessList = ['rating', 'price', 'brand']
    for item in filterList:
        if item['query_name'] in accessList:
            filterListChoose.append(item)
    return jsonify(filterListChoose)

@app.route('/<urlKeyProduct>', methods=['GET'])
def getProduct(urlKeyProduct):
    items = productDB.find_one({'url_key': urlKeyProduct}, {'_id': 0})
    return render_template('web/product.html', items=items)

@app.route('/shoppingCart', methods=['GET', 'POST', 'DELETE'])
def cart():
    userID = session.get('userID')
    if request.method == 'GET':
        userCart = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
        return render_template('web/shoppingCart.html', items = userCart['shoppingCart'])
    
    if request.method == 'POST':
        data = request.get_json()
        productID, quantity = int(data.get('id')), int(data.get('quantity'))
        product = productDB.find_one({'id': productID}, {'_id': 0})
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        existItem = accountDB.find_one({'_id': ObjectId(userID), 'shoppingCart.id': productID})

        if existItem:
            existProduct = next((item for item in existItem['shoppingCart'] if item['id'] == productID), None)
            newQuantity = existProduct['quantity'] + quantity

            if newQuantity == 0:
                accountDB.update_one(
                    {'_id': ObjectId(userID), 'shoppingCart.id': productID},
                    {'$pull': {'shoppingCart': existProduct}}
                )
                return jsonify({'message': 'Product removed from the cart successfully'}), 201

            else:
                queryAddItem = {
                    'id': existProduct['id'],
                    'name': existProduct['name'],
                    'brand': existProduct['brand'],
                    'orginalPrice': existProduct['orginalPrice'],
                    'price': existProduct['price'],
                    'quantity': newQuantity,
                    'total': newQuantity * existProduct['price'],
                    'image': existProduct['image'],
                    'url': existProduct['url'],
                    'timeAdd': datetime.now(),
                }

                accountDB.update_one(
                    {'_id': ObjectId(userID), 'shoppingCart.id': productID},
                    {'$set': {'shoppingCart.$': queryAddItem}}
                )

                if quantity > 0:
                    return jsonify({'message': 'Product added to the cart successfully'}), 201
                else:
                    return jsonify({'message': 'Product removed from the cart successfully'}), 201     
        else:
            queryAddItem = {
                'id': productID,
                'name': product['name'],
                'brand': product['brand_name'],
                'orginalPrice': product['original_price'],
                'price': product['price'],
                'quantity': quantity,
                'total': quantity * product['price'],
                'image': product['thumbnail_url'],
                'url': product['url_key'],
                'timeAdd': datetime.now(),
            }

            accountDB.update_one(
                {'_id': ObjectId(userID)},
                {'$push': {'shoppingCart': queryAddItem}}
            )
            return jsonify({'message': 'Product added to the cart successfully'}), 201
        
    if request.method == 'DELETE':
        accountDB.update_one({'_id': ObjectId(userID)}, {"$set": {"shoppingCart": []}})
        return jsonify({'message': 'All product removed from the cart successfully'}), 201
               
@app.route('/infoCustomer')
def infoCustomer():
    userID = session.get('userID')
    userCart = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
    if userCart:
        return jsonify({'user': userCart})
    else:
        return jsonify({'user': "Chưa đăng nhập"})

@app.route('/user/<option>', methods=['GET', 'POST'])
def user(option):
    userID = session.get('userID')

    sidebar = [
        ['Thông tin tài khoản', 'account'], 
        ['Đơn hàng đang xử lý', 'processing'],
        ['Đơn hàng đang vận chuyển', 'transit'],
        ['Đơn hàng đã giao', 'confirmed'],
        ['Đánh giá sản phẩm', 'review'],
        ['Sản phẩm đã xem', 'watch']
    ]

    if request.method == 'GET':
        if option == 'account':
            user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
            return render_template('web/user.html', user = user, sideBar = sidebar, title = 'Thông tin tài khoản')
        if option == 'processing':
            user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
            return render_template('web/user.html', orderList = user['orderProcessing'], sideBar = sidebar, title = 'Đơn hàng đang xử lý')   
        if option == 'transit':
            user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
            return render_template('web/user.html', orderList = user['orderTransit'], sideBar = sidebar, title = 'Đơn hàng đang vận chuyển')   
        if option == 'confirmed':
            user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
            return render_template('web/user.html', orderList = user['orderList'], sideBar = sidebar, title = 'Đơn hàng đã giao')    
        if option == 'review':
            user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
            return render_template('web/user.html', user = user, sideBar = sidebar, title = 'Đánh giá sản phẩm')    
        if option == 'watch':
            user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})
            return render_template('web/user.html', user = user, sideBar = sidebar, title = 'Sản phẩm đã xem')
        
@app.route('/buyItems', methods = ['GET', 'POST'])
def buyItems():
    userID = session.get('userID')
    user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})

    if request.method == 'GET':    
        return user['orderList']
    
    if request.method == 'POST':
        data = request.get_json()
        info = data.get('info')
        orderList = {
            'orderID': generate_order_id(),
            'buyTime': datetime.now(),
            'detail': [] 
        }

        for item in info:
            productID = int(item.split(' - ')[-1])
            product = accountDB.find_one({'shoppingCart.id': productID}, {'_id': 0, 'shoppingCart.$': 1})
            product = product['shoppingCart'][0]

            orderList['detail'].append({
                'id': product['id'],
                'name': product['name'],
                'brand': product['brand'],
                'price': product['price'],
                'quantity': product['quantity'],
                'total': product['total'],
                'image': product['image'],
                'url': product['url'],
            })
            
            accountDB.update_one(
                {'_id': ObjectId(userID)},
                {"$pull": {"shoppingCart": {"id": product['id']}}}
            )

        accountDB.update_one(
            {'_id': ObjectId(userID)},
            {'$push': {'orderProcessing': orderList}}
        )

        return jsonify({'message': 'Products added to the orderProcessing successfully'}), 201
    
def generate_order_id():
    order_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{'{:06}'.format(random.randint(0,999999))}"
    return order_id


@app.route('/processItems', methods=['GET', 'POST'])
def processItems():
    userID = session.get('userID')
    user = accountDB.find_one({'_id': ObjectId(userID)}, {'_id': 0})

    if request.method == 'GET':    
        return user['orderList']
    
    if request.method == 'POST':
        data = request.get_json()
        info = data.get('info')
        return jsonify({'message': 'Products added to the orderProcessing successfully'}), 201

@app.route('/search')
def search():
    q = request.args.get('q')
    originList = generate_substrings(q)
    origin = '|'.join(originList)
    numberItemsPerPage = 24
    percentList = []
    itemsFiltered = []

    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    
    items = list(productDB.find({"name": {"$regex": origin}}, {'_id': 0}))
    for text in items:
        originListLower = map(lambda a: a.lower(), originList)

        percent = calculate(originListLower, text['name'].lower(), len(originList))
        if percent > 0.1:
            itemsFiltered.append(text)
            percentList.append(percent)

    sorted_pairs = sorted(zip(itemsFiltered, percentList), key=lambda x: x[1], reverse=True)
    itemsSorted = [pair[0] for pair in sorted_pairs]
    
    maxPage = math.ceil(len(itemsSorted) / numberItemsPerPage)
    if page > maxPage:
        return render_template('web/404.html')
    
    list_items = [{
        'id': item['id'],
        'spid': item['spid'],
        'name': item['name'], 
        'price': item['price'], 
        'discountRate': item['discount_rate'], 
        'urlKey': item['url_key'], 
        'image': item['thumbnail_url'], 
        'quantity': item['quantity_sold'],
        'rating': item['rating_average'], 
    } for item in list(itemsSorted)[(page - 1) * numberItemsPerPage : (page) * numberItemsPerPage]]
    
    return render_template(
        'web/search.html', 
        data = list_items,
        paging = createPaging(page, maxPage, len(itemsSorted), numberItemsPerPage),
        keyword = q,
        quantityKeyword = len(itemsSorted)
    )
    
def generate_substrings(originText):
    substrings = []
    words = originText.split()
    if len(words) > 1:
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                substring = ' '.join(words[i:j])
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
    score = 0
    wordSingle = 0
    wordMulti = 0
    wordOrigin = 0

    for word in originList:
        wordOrigin += len(word)
        if (nameProduct.startswith(word + ' ') or nameProduct.endswith(' ' + word) or ' ' + word + ' ' in nameProduct):
            wordSingle += len(word)
            wordMulti += 1
            continue

    score = round(((wordSingle / wordOrigin) * (wordMulti / lenOriginList)), 2) 
    return score

@app.route('/commentUser', methods = ['GET', 'POST'])
def commentUser():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        try:
            data = request.get_json()
            text_comment = data['textComment']
            score_comment = int(data['scoreComment'])
            time_comment = data['timeComment']
            
            comments = []
            comments.append({
                'textComment': text_comment,
                'scoreComment': score_comment,
                'timeComment': time_comment
            })

            accountDB.update_one(
                {'_id': user['_id']}, 
                {'$set': {'LoginTime': datetime.now()}
            })

            return jsonify({
                'success': True, 
                'message': 'Comment added successfully', 
                'comments': comments
            })
        
        except Exception as e:
            return jsonify({
                'success': False, 
                'message': str(e)
            })

@app.route('/similar_product/<product_id>', methods = ['GET', 'POST'])
def getSimilarProduct(product_id):
    lst = []
    original = productDB.find_one({'id': int(product_id)})
    productList = productDB.find({'category': original['category']}, {'_id': 0})

    for product in productList:
        similarity_score = calculate_similarity(original['name'], product['name'])
        if similarity_score > 0.2 and similarity_score < 1:
            lst.append((round(similarity_score, 5), product))

    sortedList = sorted(lst, key=lambda x: x[0], reverse=True)

    if (len(sortedList) > 6):
        result = [
            {
                'id': item[1]['id'],
                'spid': item[1]['spid'],
                'name': item[1]['name'], 
                'price': item[1]['price'], 
                'discountRate': item[1]['discount_rate'], 
                'urlKey': item[1]['url_key'], 
                'imgUrl': item[1]['thumbnail_url'], 
                'quantitySold': item[1]['quantity_sold'],
                'rating': item[1]['rating_average'], 
            } for item in sortedList[:10]
        ]
        
        return result
    else:
        result = [
            {
                'id': item[1]['id'],
                'spid': item[1]['spid'],
                'name': item[1]['name'], 
                'price': item[1]['price'], 
                'discountRate': item[1]['discount_rate'], 
                'urlKey': item[1]['url_key'], 
                'imgUrl': item[1]['thumbnail_url'], 
                'quantitySold': item[1]['quantity_sold'],
                'rating': item[1]['rating_average'], 
            } for item in sortedList
        ]
        
        return result

def calculate_similarity(text1, text2):
        vectorizer = CountVectorizer().fit_transform([text1, text2])
        similarity = cosine_similarity(vectorizer)
        return similarity[0, 1]

if __name__ == '__main__':
    app.run(debug=True)
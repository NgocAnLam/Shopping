var product_sidebar_add = document.getElementById('product_sidebar_add');
var product_sidebar_remove = document.getElementById('product_sidebar_remove');
var product_sidebar_update = document.getElementById('product_sidebar_update');

product_sidebar_add.onclick = function() {
    window.location.href = 'http://127.0.0.1:5000/admin/product/add';
}

product_sidebar_remove.onclick = function() {
    window.location.href = 'http://127.0.0.1:5000/admin/product/remove';
}

product_sidebar_update.onclick = function() {
    window.location.href = 'http://127.0.0.1:5000/admin/product/update';
}


var btnAddProduct = document.getElementById('btnAddProduct');
if (btnAddProduct){
    btnAddProduct.onclick = function(){
        fetch("http://127.0.0.1:5000/admin/product/add", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                name: document.getElementById('name').value, //Điện thoại OPPO Reno10 5G (8GB/256GB) - Hàng Chính Hãng
                brand_name: document.getElementById('brand_name').value,
                price: document.getElementById('price').value,
                original_price: document.getElementById('original_price').value,
                thumbnail_url: document.getElementById('thumbnail_url').value,
                category: document.getElementById('category').value,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert('Product added successfully');
        })
        .catch(error => {console.error('GET request error:', error)});
    }
}


var search_input = document.getElementById('search_input');
var optionList = document.getElementById('option');
var showList = document.getElementById('showList');

if (search_input){
    search_input.addEventListener('keyup', function(){
        fetch("http://127.0.0.1:5000/admin/product/remove/getSuggestion", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'query': search_input.value,
                'option': optionList.value,
            })
        })
        .then(response => response.json())
        .then(data => { 
            showList.innerHTML = '';

            for (var i = 0; i < data['data'].length; i++){
                var option = document.createElement('option');
                option.value = data['data'][i][optionList.value];
                option.textContent = data['data'][i][optionList.value];
                showList.appendChild(option);
            }
        })
        .catch(error => {console.error('GET request error:', error)});
    });
}

var searchRemove = document.getElementById('searchRemove');
var searchUpdate = document.getElementById('searchUpdate');
var showDetailProduct = document.getElementById('showDetailProduct');

if (searchRemove){
    searchRemove.onclick = function() {
        fetch("http://127.0.0.1:5000/admin/product/remove/getProduct", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': optionList.value,
                'dataProduct': showList.value,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            showDetailProduct.innerHTML = '';
            var data = data.data;
    
            var table = document.createElement("table");
            table.style.width = "90%";
            table.style.margin = "20px";
    
            function addTrTag(labelData, valueData){
                var tr = document.createElement("tr");
            
                var label = document.createElement("td");
                label.style.width = '200px';
                label.style.paddingLeft = '10px';
                label.textContent = labelData;
                tr.appendChild(label);
            
                var value = document.createElement("td");
                value.style.paddingLeft = '10px';
                value.textContent = valueData;
                tr.appendChild(value);
            
                table.appendChild(tr);
            }
    
            addTrTag('Name', data['name']);
            addTrTag('ID', data['id']);
            addTrTag('Brand', data['brand_name']);
            addTrTag('Price', data['price']);
            addTrTag('Original Price', data['original_price']);
            addTrTag('Quantity', data['quantity_sold']);
            addTrTag('Rating', data['rating_average']);
            addTrTag('Category', data['category']);
            
    
            var btnRemove = document.createElement('button');
            btnRemove.id = 'btnRemoveProduct';
            btnRemove.textContent = 'Remove';
    
            btnRemove.onclick = function() {
                fetch("http://127.0.0.1:5000/admin/product/remove/removeProduct", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        'option': optionList.value,
                        'dataProduct': showList.value,
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    alert(data['message']);
                })
                .catch(error => {console.error('GET request error:', error)});
            };
    
            showDetailProduct.appendChild(table);
            showDetailProduct.appendChild(btnRemove);
        })
        .catch(error => {console.error('GET request error:', error)});
    };
}

if (searchUpdate){
    searchUpdate.onclick = function() {
        fetch("http://127.0.0.1:5000/admin/product/update/getProduct", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': optionList.value,
                'dataProduct': showList.value,
            })
        })
        .then(response => response.json())
        .then(data => {
            showDetailProduct.innerHTML = '';
            var data = data.data;
    
            var table = document.createElement("table");
            table.style.width = "90%";
            table.style.margin = "20px";
    
            function addTrTag(labelData, valueData = ''){
                var tr = document.createElement("tr");
            
                var label = document.createElement("td");
                label.style.width = '200px';
                label.style.paddingLeft = '10px';
                label.textContent = labelData;
                tr.appendChild(label);
            
                var value = document.createElement("td");
                var input = document.createElement("input");
                input.type = "text";
                input.className = 'textUpdate';
                input.value = valueData;
                value.append(input);
                tr.appendChild(value);
            
                table.appendChild(tr);
            }
    
            addTrTag('Name', data['name']);
            addTrTag('ID', data['id']);
            addTrTag('Brand', data['brand_name']);
            addTrTag('Price', data['price']);
            addTrTag('Original Price', data['original_price']);
            addTrTag('Category', data['category']);
            
            var btnUpdate = document.createElement('button');
            var textUpdate = document.getElementsByClassName('textUpdate');
            btnUpdate.id = 'btnUpdateProduct';
            btnUpdate.textContent = 'Update';
    
            btnUpdate.onclick = function() {
                var oldID = data['id'];
                var newID = parseInt(textUpdate[1].value);
                var newprice = parseInt(textUpdate[3].value);
                var newOriginalPrice = parseInt(textUpdate[4].value);
                var newCategory = parseInt(textUpdate[5].value);

                data['name'] = textUpdate[0].value;
                data['id'] = newID;
                data['brand_name'] = textUpdate[2].value;
                data['price'] = newprice;
                data['original_price'] = newOriginalPrice;
                data['category'] = newCategory;
                data['discount'] = newOriginalPrice - newprice;
                data['discount_rate'] = 100 - parseInt(newprice / newOriginalPrice * 100);

                fetch("http://127.0.0.1:5000/admin/product/update/updateProduct", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        'info': data,
                        'id': oldID
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    alert(data['query']);
                })
                .catch(error => {console.error('GET request error:', error)});
            };
    
            showDetailProduct.appendChild(table);
            showDetailProduct.appendChild(btnUpdate);
        })
        .catch(error => {console.error('GET request error:', error)});
    };
}


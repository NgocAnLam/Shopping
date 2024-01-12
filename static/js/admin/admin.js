function numberWithDots(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function numberWithoutDots(number) {
    return parseInt(number.replace(/\./g, ''), 10);
}

// logout processing ----------------------------------------------------
var logout = document.getElementById('logout');
logout.onclick = function(){
    fetch('http://127.0.0.1:5000/admin/logout', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
    })
    .then(response => response.json())
    .then(data => {window.location.href = 'http://127.0.0.1:5000/admin/login'})
    .catch(error => {console.error('GET request error:', error)});
}

// Dashboard ----------------------------------------------------------------

var dashboard = document.getElementById('dashboard_sidebar');
dashboard.onclick = function (){alert('dashboard clicked');}

// Customer ----------------------------------------------------------------

var customer = document.getElementById('customer_sidebar');
customer.onclick = function (){
    window.location.href = 'http://127.0.0.1:5000/admin/customer'
    fetch('http://127.0.0.1:5000/admin/customer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
    })
    .then(response => response.json())
    .then(data => {})
    .catch(error => {console.error('GET request error:', error)});
}

// Product ----------------------------------------------------------------

var product = document.getElementById('product_sidebar');
product.onclick = function (){
    window.location.href = 'http://127.0.0.1:5000/admin/product';
    fetch('http://127.0.0.1:5000/admin/product')
    .then(response => response.json())
    .then(data => {})
    .catch(error => {console.error('GET request error:', error)});
}

// Process ----------------------------------------------------------------

var processing = document.getElementById('processing_sidebar');
processing.onclick = function (){
    window.location.href = 'http://127.0.0.1:5000/admin/process';
    fetch('http://127.0.0.1:5000/admin/process')
    .then(response => response.json())
    .then(data => {console.log(data)})
    .catch(error => {console.error('GET request error:', error)});
}

// Transit ----------------------------------------------------------------

var transit = document.getElementById('transit_sidebar');
transit.onclick = function (){
    window.location.href = 'http://127.0.0.1:5000/admin/transit';
    fetch('http://127.0.0.1:5000/admin/transit')
    .then(response => response.json())
    .then(data => {console.log(data)})
    .catch(error => {console.error('GET request error:', error)});
}

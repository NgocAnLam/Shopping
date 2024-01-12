var customer_sidebar_info = document.getElementById('customer_sidebar_info');
var customer_sidebar_process = document.getElementById('customer_sidebar_process');
var customer_sidebar_transit = document.getElementById('customer_sidebar_transit');
var customer_sidebar_confirm = document.getElementById('customer_sidebar_confirm');

var urlParams = new URLSearchParams(window.location.search);
var customerID = urlParams.get('id');
var baseurl = 'http://127.0.0.1:5000/admin/customer';

customer_sidebar_info.onclick = function(){window.location.href = `${baseurl}?id=${customerID}&option=info`}
customer_sidebar_process.onclick = function(){window.location.href = `${baseurl}?id=${customerID}&option=process`}
customer_sidebar_transit.onclick = function(){window.location.href = `${baseurl}?id=${customerID}&option=transit`}
customer_sidebar_confirm.onclick = function(){window.location.href = `${baseurl}?id=${customerID}&option=confirm`}

var priceList = document.querySelectorAll('.price')

function numberWithDots(number) {return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")}
function numberWithoutDots(number) {return parseInt(number.replace(/\./g, ''), 10)}

for (var i = 0; i < priceList.length; i++){
    priceList[i].textContent = numberWithDots(priceList[i].textContent) + "đ";
}


var btnConfirmProcess = document.querySelectorAll('.btnConfirmProcess');

for (var i = 0; i < btnConfirmProcess.length; i++){
    console.log(btnConfirmProcess[i]);
}

var time = document.querySelectorAll('.time');
for (var i = 0; i < time.length; i++){
    time[i].textContent = time[i].textContent.split('.')[0];
}
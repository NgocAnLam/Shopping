var priceList = document.querySelectorAll('.price')

function numberWithDots(number) {return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")}
function numberWithoutDots(number) {return parseInt(number.replace(/\./g, ''), 10)}

for (var i = 0; i < priceList.length; i++){
    priceList[i].textContent = numberWithDots(priceList[i].textContent) + "đ";
}


var btnConfirmProcess = document.querySelectorAll('.btnConfirmProcess');
var orderIDList = document.querySelectorAll('.orderID');
var customerIDList = document.querySelectorAll('.infoCustomer');

for (var i = 0; i < btnConfirmProcess.length; i++){
    btnConfirmProcess[i].addEventListener("click", (function(index) {
        return function() {
            var orderIDPost = orderIDList[index].textContent.split(" ")[2];
            var customerIDPost = customerIDList[index].textContent.split(" ")[2];          
            fetch("http://127.0.0.1:5000/admin/order/process/" + customerIDPost + '/' + orderIDPost, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                location.reload();
            })
            .catch(error => {console.error('GET request error:', error)});
        };
    })(i));
}
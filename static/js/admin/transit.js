var priceList = document.querySelectorAll('.price')

function numberWithDots(number) {return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")}
function numberWithoutDots(number) {return parseInt(number.replace(/\./g, ''), 10)}

for (var i = 0; i < priceList.length; i++){
    priceList[i].textContent = numberWithDots(priceList[i].textContent) + "đ";
}


var btnConfirmTransit = document.querySelectorAll('.btnConfirmTransit');
var orderIDList = document.querySelectorAll('.orderID');
var customerIDList = document.querySelectorAll('.infoCustomer');

for (var i = 0; i < btnConfirmTransit.length; i++){
    btnConfirmTransit[i].addEventListener("click", (function(index) {
        return function() {
            var orderIDPost = orderIDList[index].textContent.split(" ")[2];
            var customerIDPost = customerIDList[index].textContent.split(" ")[2];          
            fetch("http://127.0.0.1:5000/admin/transit/" + customerIDPost + '/' + orderIDPost, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
            })
            .then(response => response.json())
            .then(data => {location.reload()})
            .catch(error => {console.error('GET request error:', error)});
        };
    })(i));
}
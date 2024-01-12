var btnMinus = document.getElementById('minus');
var btnPlus = document.getElementById('plus');
var divQuantityProduct = document.getElementById('quantity');
var itemPrice = document.getElementById('itemPrice');
var calculatePrice = document.getElementById('calculatePrice');
var divDescription = document.getElementById('divDescription');
var btnAddToCart = document.getElementById('btnAddToCart');

// Initial Function
function numberWithDots(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function numberWithoutDots(number) {
    return parseInt(number.replace(/\./g, ''), 10);
}

// Initial Processing
itemPrice.textContent = numberWithDots(itemPrice.textContent);
calculatePrice.textContent = itemPrice.textContent;

divDescription.textContent = divDescription.textContent.replace(new RegExp('width="750"', 'g'), 'width="100%"')
divDescription.textContent = divDescription.textContent.replace(/height="\d+"/g, 'height="auto"');
divDescription.innerHTML = divDescription.textContent;

// add event handlers
btnMinus.addEventListener("click", function() {
    var currentQuantity = parseInt(divQuantityProduct.textContent) - 1;
    var unitPrice = numberWithoutDots(itemPrice.textContent);
    if (currentQuantity > 0){
        divQuantityProduct.textContent = currentQuantity.toString();
        calculatePrice.textContent = numberWithDots(unitPrice * currentQuantity) + 'đ';
    }
});

btnPlus.addEventListener("click", function() {
    var currentQuantity = parseInt(divQuantityProduct.textContent) + 1;
    var unitPrice = numberWithoutDots(itemPrice.textContent);
    divQuantityProduct.textContent = currentQuantity.toString();
    calculatePrice.textContent = numberWithDots(unitPrice * currentQuantity) + 'đ';
});

btnAddToCart.addEventListener("click", function() {
    var divNotificationAddToCart = document.createElement("div");
    divNotificationAddToCart.id = "notificationAddToCart";
    divNotificationAddToCart.textContent = "Đã thêm vào giỏ hàng";
    divNotificationAddToCart.style.marginTop = "30px";
    divNotificationAddToCart.style.padding = "20px";
    divNotificationAddToCart.style.width = "300px";
    divNotificationAddToCart.style.height = "fit-content";
    divNotificationAddToCart.style.backgroundColor = "#81cf8c";
    btnAddToCart.appendChild(divNotificationAddToCart);
    setTimeout(function (){btnAddToCart.removeChild(divNotificationAddToCart)}, 3000);

    var pathnameURL = (window.location.pathname).split('-');
    var productID = pathnameURL[pathnameURL.length - 1].slice(1);

    fetch("http://127.0.0.1:5000/shoppingCart", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            id: productID, 
            quantity: divQuantityProduct.textContent,
        })
    })
    .then(response => response.json())
    .then(data => {console.log(data)})
    .catch(error => {console.error('GET request error:', error)});
});


var infoUser = document.getElementById('infoUser');
fetch("http://127.0.0.1:5000/info")
.then(response => response.json())
.then(data => {
    console.log(data);
    infoUser.textContent = data.username;
})
.catch(error => {console.error('GET request error:', error)});


var minusRating = document.getElementById('minusRating');
var plusRating = document.getElementById('plusRating');
var scoreRating = document.getElementById('scoreRating');
var postUser = document.getElementById('postUser');
var writeUser = document.getElementById('writeUser');

minusRating.onclick = function () {
    score = parseInt(scoreRating.textContent);
    if (score > 1){scoreRating.textContent =  score - 1}
}

plusRating.onclick = function () {
    score = parseInt(scoreRating.textContent);
    if (score < 5){scoreRating.textContent = score + 1}
}

postUser.onclick = function () {
    fetch("http://127.0.0.1:5000/commentUser", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            textComment: writeUser.value,
            scoreComment: scoreRating.textContent,
            timeComment: getDateTime()
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {console.error('GET request error:', error)});
}

function getDateTime(){
    var currentDate = new Date();
    var year = currentDate.getFullYear();
    var month = currentDate.getMonth()+1;
    var day = currentDate.getDate();
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var seconds = currentDate.getSeconds();
    var milliseconds = currentDate.getMilliseconds();
    let Time = year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds + ':' + milliseconds;
    return Time;
}


  
//   div.scrollmenu a {
//     display: inline-block;
//     color: white;
//     text-align: center;
//     padding: 14px;
//     text-decoration: none;
//   }
  
//   div.scrollmenu a:hover {
//     background-color: #777;
//   }


var similarProduct = document.getElementById('similarProduct');
var productID = window.location.pathname.split('-').slice(-1);
console.log(productID);
fetch("http://127.0.0.1:5000/similar_product/" + window.location.pathname.split('-p').slice(-1))
.then(response => response.json())
.then(data => {
    console.log(data);
    similarProduct.innerHTML = '';
    similarProduct.style.margin = '20px 10px';
    similarProduct.style.width = '100%';


    for (var i=0; i<data.length; i++) {
        var divProduct = document.createElement('div');
        divProduct.className = 'card';
        divProduct.style.margin = '10px 10px 10px 0px';
        divProduct.style.padding = '10px';
        divProduct.style.width = '300px';
        divProduct.style.height = '500px';
        divProduct.style.borderRadius = '10px';

        var link = document.createElement('a');
        link.href = 'http://127.0.0.1:5000/' + data[i]['urlKey']

        var image = document.createElement('img');
        image.className = "card-img";
        image.src = data[i]['imgUrl'];
        image.width = "200px";
        image.height = "300";

        var cardBody = document.createElement('div');
        cardBody.className = "card-body";

        var title = document.createElement('p');
        title.className = "card-title";
        title.style.width = "100%";
        title.style.height = "50px";
        title.style.overflow = "hidden";
        title.style.whiteSpace = "wrap";
        title.style.textOverflow = "ellipsis";
        title.textContent = data[i]['name'];

        cardBody.appendChild(title);

        var evaluate = document.createElement('div');
        evaluate.className = "d-flex flex-column evaluate";
        cardBody.appendChild(evaluate);
        
        var evaluate_price_discount = document.createElement('div');
        evaluate_price_discount.className = "d-flex flex-row";

        var price = document.createElement('p');
        price.className = "card-price";
        price.textContent = numberWithDots(data[i]['price']) + 'đ';
        price.style.marginRight = "50px";
        evaluate_price_discount.appendChild(price);

        var discount = document.createElement('p');
        discount.className = "card-discount";
        discount.textContent = '-' + data[i]['discountRate'] + '%';
        evaluate_price_discount.appendChild(discount);

        evaluate.appendChild(evaluate_price_discount);

        var evaluate_star_quantity = document.createElement('div');
        evaluate_star_quantity.className = "d-flex flex-row";

        var star = document.createElement('p');
        star.className = "star";
        star.textContent = 'Đánh giá: ' + data[i]['rating'];
        star.style.marginRight = "30px";
        evaluate_star_quantity.appendChild(star);

        var quantity = document.createElement('p');
        quantity.className = "quantity";
        quantity.textContent = 'Đã bán: ' + data[i]['quantitySold'];
        evaluate_star_quantity.appendChild(quantity);

        evaluate.appendChild(evaluate_star_quantity);

        divProduct.appendChild(image);
        divProduct.appendChild(cardBody);
        link.appendChild(divProduct);
        similarProduct.appendChild(link);
    }
})
.catch(error => {console.error('GET request error:', error)});
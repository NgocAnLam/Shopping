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

if (divDescription){
    divDescription.textContent = divDescription.textContent.replace(new RegExp('width="750"', 'g'), 'width="100%"')
    divDescription.textContent = divDescription.textContent.replace(/height="\d+"/g, 'height="auto"');
    divDescription.innerHTML = divDescription.textContent;
}


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
    fetch("http://127.0.0.1:5000/info")
    .then(response => response.json())
    .then(data => {
        if (data['isLogin'] == true){
            var notiAddToCart = document.createElement("div");
            notiAddToCart.id = "notiAddToCart";
            notiAddToCart.textContent = "Đã thêm vào giỏ hàng";
            btnAddToCart.appendChild(notiAddToCart);
            setTimeout(function (){btnAddToCart.removeChild(notiAddToCart)}, 3000);

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
        }
        else {window.location.href = "http://127.0.0.1:5000/login";}
    })
    .catch(error => {console.error('GET request error:', error)}); 
});

var minusRating = document.getElementById('minusRating');
var plusRating = document.getElementById('plusRating');
var scoreRating = document.getElementById('scoreRating');
var postUser = document.getElementById('postUser');
var writeUser = document.getElementById('writeUser');

if (minusRating){
    minusRating.onclick = function () {
        score = parseInt(scoreRating.textContent);
        if (score > 1){scoreRating.textContent =  score - 1}
    }
}

if (plusRating){
    plusRating.onclick = function () {
        score = parseInt(scoreRating.textContent);
        if (score < 5){scoreRating.textContent = score + 1}
    }
}

fetch("http://127.0.0.1:5000/info")
.then(response => response.json())
.then(data => {
    var email = data['email'];
    if (email == null && postUser){postUser.disabled = true;}
    if (email != null && postUser) {postUser.disabled = false}
})
.catch(error => {console.error('GET request error:', error)});

if (postUser){
    postUser.onclick = function () {
        fetch("http://127.0.0.1:5000/info")
        .then(response => response.json())
        .then(data => {
            var email = data['email'];
            var username = data['username'];
            var productID = window.location.pathname.split('-p').slice(-1)[0];
    
            fetch("http://127.0.0.1:5000/getComment/" + productID, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    comment: writeUser.value,
                    score: scoreRating.textContent,
                    email: email,
                    username: username,
                    type: 'add'
                })
            })
            .then(response => response.json())
            .then(data => {window.location.reload()})
            .catch(error => {console.error('GET request error:', error)});
        })
        .catch(error => {console.error('GET request error:', error)});
    }    
}


var showComment = document.getElementById('showComment');
var product_id = window.location.pathname.split('-p').slice(-1)[0];

fetch("http://127.0.0.1:5000/getComment/" + product_id)
.then(response => response.json())
.then(data => {
    var comment = data['comments'];
    showComment.innerHTML = '';
    console.log(comment);
    for (var i = 0; i < comment.length; i++) {
        var divComment = document.createElement('div');
        divComment.className = 'd-flex flex-row';
        divComment.style.margin = '10px';

        var username = document.createElement('div');
        username.textContent = comment[i]['username'];
        username.style.minWidth = '150px';
        username.style.maxWidth = '150px';
        divComment.appendChild(username);

        var commentText = document.createElement('div');
        commentText.textContent = comment[i]['comment'];
        commentText.style.minWidth = '600px';
        commentText.style.maxWidth = '600px';
        divComment.appendChild(commentText);

        var score = document.createElement('div');
        score.textContent = comment[i]['score'] + ' sao';
        score.style.minWidth = '100px';
        score.style.maxWidth = '100px';
        divComment.appendChild(score);

        var comment_date = document.createElement('div');
        var comment_time = comment[i]['time'];
        var originalDate = new Date(comment_time);
        var date = originalDate.getDate().toString().padStart(2, '0');
        var month = (originalDate.getMonth() + 1).toString().padStart(2, '0');
        var year = originalDate.getFullYear();
        var hour = originalDate.getHours().toString().padStart(2, '0');
        var minute = originalDate.getMinutes().toString().padStart(2, '0');
        var second = originalDate.getSeconds().toString().padStart(2, '0');
        comment_date.textContent = `${date}-${month}-${year} ${hour}:${minute}:${second}`;
        divComment.appendChild(comment_date);

        showComment.appendChild(divComment);
    }
})
.catch(error => {console.error('GET request error:', error)});


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

var similarProduct = document.getElementById('similarProduct');
var productID = window.location.pathname.split('-').slice(-1);

fetch("http://127.0.0.1:5000/similar_product/" + window.location.pathname.split('-p').slice(-1))
.then(response => response.json())
.then(data => {
    similarProduct.innerHTML = '';
    similarProduct.style.margin = '20px 10px';
    similarProduct.style.width = '100%';

    for (var i = 0; i < data.length; i++) {
        var divProduct = document.createElement('div');
        divProduct.className = 'card';
        
        var link = document.createElement('a');
        link.href = 'http://127.0.0.1:5000/' + data[i]['urlKey']

        var image = document.createElement('img');
        image.className = "card-img";
        image.src = data[i]['imgUrl'];

        var cardBody = document.createElement('div');
        cardBody.className = "card-body";

        var title = document.createElement('p');
        title.className = "card-title";
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


var btnBuyNow = document.getElementById('btnBuyNow');

btnBuyNow.addEventListener("click", function() {
    fetch("http://127.0.0.1:5000/info")
    .then(response => response.json())
    .then(data => {
        if (data['isLogin'] == true) {
            var product_name = window.location.pathname;
            var product_id = parseInt(product_name.split('-p')[product_name.split('-p').length - 1]);
            var quantity = parseInt(document.getElementById('quantity').textContent);

            fetch("http://127.0.0.1:5000/buy_now/" + product_id + "/" + quantity, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                var notiBuyNow = document.createElement("div");
                notiBuyNow.id = "notiBuyNow";
                notiBuyNow.textContent = "Đã mua sản phẩm";
                btnBuyNow.appendChild(notiBuyNow);
                setTimeout(function (){btnBuyNow.removeChild(notiBuyNow)}, 3000);
            })
            .catch(error => {console.error('GET request error:', error)});
        }
        else {window.location.href = "http://127.0.0.1:5000/login";}
    })
    .catch(error => {console.error('GET request error:', error)}); 
});
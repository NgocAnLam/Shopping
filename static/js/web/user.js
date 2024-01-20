var date = document.getElementsByClassName('date');
var price = document.getElementsByClassName('price');


function numberWithDots(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

for (var i = 0; i < date.length; i++) {
    date[i].textContent = date[i].textContent.split('.')[0];
}

for (var i = 0; i < price.length; i++) {
    price[i].textContent = numberWithDots(price[i].textContent) + 'đ';
}


var btnComment = document.querySelectorAll('.btnComment');
var product_id = document.querySelectorAll('.productIDOrder');

for (let i = 0; i < btnComment.length; i++) {
    btnComment[i].addEventListener("click", function () {

        fetch("http://127.0.0.1:5000/info")
        .then(response => response.json())
        .then(data => {
            var email = data['email'];
            if (email != null) {
                var productID = product_id[i].textContent;

                fetch("http://127.0.0.1:5000/product/" + productID)
                .then(response => response.json())
                .then(data => {})
                .catch(error => {console.error('GET request error:', error)});
            }
        })
        .catch(error => {console.error('GET request error:', error)});  
    });
}






       


// if (plus){
//     plus.onclick = function(){
//         var star = document.getElementById("star");
//         if (parseInt(star.textContent) < 5){
//             star.textContent = (parseInt(star.textContent) + 1).toString();
//         }
//     }
// }



        


      
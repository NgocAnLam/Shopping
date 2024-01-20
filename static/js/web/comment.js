var price = document.getElementById('price');
var minus = document.getElementById('minus');
var plus = document.getElementById('plus');
var score = document.getElementById('score');
var btnPostComment = document.getElementById('btnPostComment');
var input = document.getElementById('input');


function numberWithDots(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function numberWithoutDots(number) {
    return parseInt(number.replace(/\./g, ''), 10);
}

price.textContent = 'Price: ' + numberWithDots(price.textContent) + 'đ';

minus.onclick = function(){
    var num_score = parseInt(score.textContent);
    if (num_score > 1){
        score.textContent = (num_score - 1).toString();
    }
}

plus.onclick = function(){
    var num_score = parseInt(score.textContent);
    if (num_score < 5){
        score.textContent = (num_score + 1).toString();
    }
}



btnPostComment.onclick = function(){
    if (input.value != ""){
        var url = window.location.href;
        fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "comment": input.value,
                "score": score.textContent,
            }), 
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            window.location.href = "http://127.0.0.1:5000/user/confirmed";
        })
        .catch(error => {console.error('GET request error:', error)});
    }
}

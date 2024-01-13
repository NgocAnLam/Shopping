function numberWithDots(number) {return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")}
function numberWithoutDots(number) {return parseInt(number.replace(/\./g, ''), 10)}

var numRevenue = document.getElementById("numRevenue");
numRevenue.textContent = numberWithDots(numRevenue.textContent) + 'đ';

// Draw --------------------------------

fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        'option': 'week',
    })
})
.then(response => response.json())
.then(data => { 
    var key = data.key;
    var value = data.value;
    drawRevenue(key, value);
})
.catch(error => {console.error('GET request error:', error)});


function drawRevenue(key, value) {
    var divCanvas = document.getElementById('canvas');
    divCanvas.innerHTML = '';
    var myChart = document.createElement('canvas');
    myChart.id = 'myChart';
    divCanvas.appendChild(myChart);

    myChart = document.getElementById('myChart').getContext('2d');
    myChart.canvas.width = 1000;
    myChart.canvas.height = 300;

    let massPopChart = new Chart(myChart, {
        type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
        data:{
            labels: key,
            datasets:[{data: value, backgroundColor: '#fea322'}]
        },
        options:{
            title: {display: true, text:'Detail Revenue', fontSize: 25},
            legend: {display: false},
        }
    });
}

var chartYear = document.getElementById('chartYear')
var chartMonth = document.getElementById('chartMonth')
var chartWeek = document.getElementById('chartWeek')
var optionMonth = document.getElementById('optionMonth')
var optionYear = document.getElementById('optionYear')
var selected = document.querySelector('.selected').textContent;
optionYear.hidden = true;
optionMonth.hidden = true;

document.addEventListener("DOMContentLoaded", function() {
    var optionTimeCharts = document.querySelectorAll('.optionTime');

    optionTimeCharts.forEach(function(chart) {
        chart.addEventListener('click', function() {
            optionTimeCharts.forEach(function(c) {c.classList.remove('selected')});
            chart.classList.add('selected');

            var selected = document.querySelector('.selected').textContent;
            if (selected == 'Year'){
                optionYear.hidden = false;
                optionMonth.hidden = true;
            }
            else if (selected == 'Month'){
                optionYear.hidden = false;
                optionMonth.hidden = false;
            }
            else {
                optionYear.hidden = true;
                optionMonth.hidden = true;
            }
        });
    });
});

optionYear.addEventListener('change', function () {
    var selected = document.querySelector('.selected').textContent;

    if (selected == 'Year') {
        fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': 'year',
                'year': optionYear.value,
            })
        })
        .then(response => response.json())
        .then(data => { 
            var key = data.key;
            var value = data.value;
            drawRevenue(key, value);
        })
        .catch(error => {console.error('GET request error:', error)});
    }
    else if (selected == 'Month'){
        fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': 'month',
                'year': optionYear.value,
                'month': optionMonth.value
            })
        })
        .then(response => response.json())
        .then(data => { 
            var key = data.key;
            var value = data.value;
            drawRevenue(key, value);
        })
        .catch(error => {console.error('GET request error:', error)});
    }
    else {
        fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': 'week',
            })
        })
        .then(response => response.json())
        .then(data => { 
            var key = data.key;
            var value = data.value;
            drawRevenue(key, value);
        })
        .catch(error => {console.error('GET request error:', error)});
    }
    
});

optionMonth.addEventListener('change', function () {
    var selected = document.querySelector('.selected').textContent;

    if (selected == 'Year') {
        fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': 'year',
                'year': optionYear.value,
            })
        })
        .then(response => response.json())
        .then(data => { 
            var key = data.key;
            var value = data.value;
            drawRevenue(key, value);
        })
        .catch(error => {console.error('GET request error:', error)});
    }
    else if (selected == 'Month'){
        fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': 'month',
                'year': optionYear.value,
                'month': optionMonth.value
            })
        })
        .then(response => response.json())
        .then(data => { 
            var key = data.key;
            var value = data.value;
            drawRevenue(key, value);
        })
        .catch(error => {console.error('GET request error:', error)});
    }
    else {
        fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                'option': 'week',
            })
        })
        .then(response => response.json())
        .then(data => { 
            var key = data.key;
            var value = data.value;
            drawRevenue(key, value);
        })
        .catch(error => {console.error('GET request error:', error)});
    }
    
});

chartYear.onclick = function(){
    fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            'option': 'year',
            'year': optionYear.value,
        })
    })
    .then(response => response.json())
    .then(data => { 
        var key = data.key;
        var value = data.value;
        drawRevenue(key, value);
    })
    .catch(error => {console.error('GET request error:', error)});
}

chartMonth.onclick = function(){
    fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            'option': 'month',
            'year': optionYear.value,
            'month': optionMonth.value
        })
    })
    .then(response => response.json())
    .then(data => { 
        var key = data.key;
        var value = data.value;
        drawRevenue(key, value);
    })
    .catch(error => {console.error('GET request error:', error)});
}

chartWeek.onclick = function(){
    fetch("http://127.0.0.1:5000/admin/dashboard/chartRevenue", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            'option': 'week',
        })
    })
    .then(response => response.json())
    .then(data => { 
        var key = data.key;
        var value = data.value;
        drawRevenue(key, value);
    })
    .catch(error => {console.error('GET request error:', error)});
}
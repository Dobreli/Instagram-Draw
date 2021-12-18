$(function() {
    if (localStorage.basket) {
        basket = JSON.parse(localStorage.basket);
        showbasket();
    }
});

function addTobasket(price, name, qty) {
    var price = price;
    var name = name;
    var qty = qty;

    for (var i in basket) {
        if (basket[i].Product == name) {
            basket[i].Qty = String(parseInt(basket[i].Qty) + parseInt(qty));
            showbasket();
            savebasket();
            return;
        }
    }
    var item = {
        Product: name,
        Price: price,
        Qty: qty
    };
    basket.push(item);
    savebasket();
    showbasket();
}

function deleteItem(index) {
    basket.splice(index, 1);
    showbasket();
    savebasket();
}

function savebasket() {
    if (window.localStorage) {
        localStorage.basket = JSON.stringify(basket);
    }
}

function showbasket() {
    $("#basketbody").empty();
    for (var i in basket) {
        var item = basket[i];
        var row = "<tr><td>" + item.Product + "</td><td>" +
            item.Price + "</td><td>" + item.Qty + "</td><td>" +
            parseInt(item.Qty) * parseInt(item.Price) + "</td><td>" +
            "<button onclick='deleteItem(" + i + ")' class='btn btn-outline-danger btn-sm'>Delete</button></td></tr>";
        $("#basketbody").append(row);
    }
}

var addbasket = document.querySelectorAll('#addbasket')
var membername = document.querySelectorAll('#member-name')
var memberprice = document.querySelectorAll('#member-price')
$(document).on('click', addbasket, function(event) {
        for (let i = 0; i < addbasket.length; i++) {
            if (event.target == addbasket[i]) {
                let price = memberprice[i].innerHTML
                let name = membername[i].innerHTML
                let qty = 1
                addTobasket(price, name, qty)
            }
        }
    })
    /*
    var basket = []; <
    main class = "main" >
        <div class = "modal fade"
    id = "shoppingbasketlist"
    data - bs - backdrop = "static"
    data - bs - keyboard = "false"
    tabindex = "-1"
    aria - labelledby = "shopping-basket-list"
    aria - hidden = "true" >
        <
        div class = "modal-dialog modal-dialog-scrollable modal-lg" >
        <
        div class = "modal-content" >
        <
        div class = "modal-header" >
        <
        h5 class = "modal-title"
    id = "staticBackdropLabel" > Sepet < /h5> <
        button type = "button"
    class = "btn-close"
    data - bs - dismiss = "modal"
    aria - label = "Close" > < /button> <
        /div> <
        div class = "modal-body modal-body-basket" >
        <
        div class = "card-table-main" >
        <
        div class = "col-12 text-center pt-2" >
        <
        h3 class = "page-title" > Sepetim < /h3> <
        /div> <
        div class = "table-responsive" >

        <
        table class = "table text-center" >
        <
        thead >
        <
        tr >
        <
        th style = "width: auto;" > Ürün < /th> <
        th style = "width: auto;" > Fiyat < /th> <
        th style = "width: auto;" > Adet < /th> <
        th style = "width: auto;" > Toplam < /th> <
        th style = "width: auto;" > < /th> <
        /tr> <
        /thead> <
        tbody id = "basketbody" >
        <
        /tbody> <
        /table> <
        /div> <
        /div> <
        /div> <
        div class = "modal-footer" >
        <
        button type = "button"
    class = "btn btn-primary" > Alışveriş Tamamla < /button> <
        button type = "button"
    class = "btn btn-secondary"
    data - bs - dismiss = "modal" > Kapat < /button> <
        /div> <
        /div> <
        /div> <
        /div>
    */

function onAddToCart(id, name, price) {
    var products = {
        "id": id,
        "name": name,
        "price": parseFloat(price)
    };

    $.ajax({
        type: "POST",
        url: "/cart",
        data: JSON.stringify(products),
        contentType: "application/json",
        dataType: "json",
        success: function(cartContents) {
            console.log(cartContents);
        }
    });
}


function continueWithAddress() {
    var address = document.getElementById("shipping-address");
    address.style.display = "block";
    var continueButton = document.getElementById("continue-button");
    continueButton.style.display="none";
}


function onViewCart() {
        $.ajax({
        type: "GET",
        url: "/cart",
        contentType: "application/json",

        success: function(cartContents) {
            var cart = JSON.parse(cartContents)
            var cartTable = document.getElementById('table-body');

            var cartModal = document.getElementById('cart-content');
            if (cart[0]['products'].length > 0) {
                cartModal.style.display = "block";

                cartTable.innerHTML = "";
                console.log(cart[0]);
                var totalPrice = 0;
                for(var i=0; i < cart[0]['products'].length; i++) {
                    totalPrice += parseFloat(cart[0]['products'][i]['total-price']);

                    cartTable.innerHTML += "<tr>" +
                        "<td>" + cart[0]['products'][i]['name'] + "</td>" +
                        "<td>£" + cart[0]['products'][i]['price'] + "</td>" +
                        "<td>" + cart[0]['products'][i]['quantity'] + "</td>" +
                        "<td>£" + cart[0]['products'][i]['total-price'] + "</td>" +
                        "</tr>"
                }
                if(totalPrice !== 0) {
                    cartTable.innerHTML += "<tr>" +
                        "<td></td>" +
                        "<td></td>" +
                        "<td>Total:</td>" +
                        "<td>£" + totalPrice + "</td>" +
                        "</tr>"
                }
            }
        }
    });
}
/**
 * Given product data, send an Ajax request to /cart to update the
 * user's cart contents.
 *
 * @param id - the product id
 * @param name - the product name
 * @param price - the product price
 */
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
        dataType: "json"
    });
}


/**
 * Send an Ajax request to delete the user's cart.
 * Reset the cart UI on completion.
 */
function clearCart() {
    $.ajax({
        type: "POST",
        url: "/cart",
        data: JSON.stringify({"delete": "delete"}),
        contentType: "application/json",
        dataType: "json",
        success: function() {
           // Reset cart modal.
            var cartModal = document.getElementById("cart-content")
            cartModal.style.display="none";
        }
    });
}


/**
 * Display the shipping address form inside of the cart modal.
 * Hide the continue button.
 */
function continueWithAddress() {
    var address = document.getElementById("shipping-address");
    address.style.display = "block";
    var continueButton = document.getElementById("continue-button");
    continueButton.style.display="none";
}


/**
 * Send an Ajax request to get the user's cart contents.
 * Build the HTML to display the cart contents.
 */
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

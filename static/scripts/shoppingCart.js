
function onAddToCart(id, name, price) {

    var products = {
        "id": id,
        "name": name,
        "price": price
    };

    $.ajax({
        type: "POST",
        url: "/cart",
        data: JSON.stringify(products),
        contentType: "application/json",
        dataType: "json",
        success: function(cartContents) {
            var cart = document.getElementById("cart-content");
            tableBody = document.getElementById("table-body")


            console.log(cartContents[0]);
        }
    });
}

function continueWithAddress() {
    var address = document.getElementById("shipping-address")
    address.style.display = "block";
    var continueButton = document.getElementById("continue-button")
    continueButton.style.display="none";
}

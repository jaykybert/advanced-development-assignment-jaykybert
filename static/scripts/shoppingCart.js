
function onAddToCart(id, name, price) {

    var products = {
        "id": id,
        "name": name,
        "price": price
    };

    console.log(products);

    $.ajax({
        type: "POST",
        url: "/cart",
        data: JSON.stringify(products),
        contentType: "application/json",
        dataType: "json",
        success: function(cartContents) {
            console.log(cartContents);
            var cart = document.getElementById("cart-content");
            cart.innerHTML = cartContents;
        }
    });
}

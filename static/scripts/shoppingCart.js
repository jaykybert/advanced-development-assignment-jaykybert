
function onAddToCart(productId) {
    $.ajax({
        type: "POST",
        url: "/cart",
        data: JSON.stringify({'id': productId}),
        contentType: "application/json",
        dataType: "json",
        success: function(result) {
            console.log('success!');
        }
    });
}

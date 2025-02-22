// Message timeout functionality
var messageTimeout = document.getElementById("message-timer");

if (messageTimeout) {  // Check if element exists before manipulating
    setTimeout(function() {
        messageTimeout.style.display = "none";
    }, 5500);
} else {
    console.log("Element #message-timer not found on this page");
}

$(document).ready(function() {
    // Assuming jQuery is loaded

    // Function to update the cart quantity display
    function updateCartDisplay(qty) {
        var cartQtyElement = document.getElementById("cart-qty");
        if (cartQtyElement) {  // Check if element exists
            cartQtyElement.textContent = qty;
        } else {
            console.log("Element #cart-qty not found");
        }
    }

    // Update button functionality
    $(document).on('click', '#update-button', function(e){
        e.preventDefault();
        var productId = $(this).val();
        var selectedQty = parseInt($('#qty').val());
        var maxStock = parseInt($('#qty').attr('max')); // Assuming 'max' attribute on qty input

        if (selectedQty > maxStock) {
            alert('Sorry, we only have ' + maxStock + ' in stock.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '{% url "cart-update" %}',
            data: {
                product_id: productId,
                product_quantity: selectedQty,
                csrfmiddlewaretoken: "{{ csrf_token }}",
                action: 'post'
            },
            success: function(json){
                if (json.success) {
                    updateCartDisplay(json.qty);
                    alert('Cart updated successfully'); // Or use a modal
                } else {
                    console.log(json.message);
                    alert(json.message);
                }
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status + ": " + xhr.responseText);
                alert('An error occurred while updating the cart. Please try again.');
            }
        });
    });

    // Delete button functionality
    $(document).on('click', '#delete-button', function(e){
        e.preventDefault();
        var productId = $(this).val();

        $.ajax({
            type: 'POST',
            url: '{% url "cart-delete" %}',
            data: {
                product_id: productId,
                csrfmiddlewaretoken: "{{ csrf_token }}",
                action: 'post'
            },
            success: function(json){
                if (json.success) {
                    updateCartDisplay(json.qty);
                    alert('Item removed from cart'); // Or use a modal
                    // Optionally refresh cart view or remove item from DOM
                } else {
                    console.log(json.message);
                    alert(json.message);
                }
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status + ": " + xhr.responseText);
                alert('An error occurred while removing from cart. Please try again.');
            }
        });
    });
});
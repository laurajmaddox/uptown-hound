/*===============================================
 shop.js
===============================================*/


$(document).ready(function () {
  
    /* Add navbar shadow on page scroll */
    $(window).scroll(function () {
        
        if ($(this).scrollTop()) {
            $('.navbar').addClass('navbar-shadow');
        } else {
            $('.navbar').removeClass('navbar-shadow');
        }
    
    });

    /* Toggle search bar in nav header */
    $('#js-search-toggle').click(function (event) {
    
        $('#js-nav-search').toggleClass('hidden');
    
        $('#js-search-toggle').children('span')
            .toggleClass('glyphicon-search')
            .toggleClass('glyphicon-remove');
    
    });

    /* Remove item from cart via Ajax POST */
    $('.js-remove-item').click(function (event) {
    
        var sku = $(event.target).closest('a').data('sku');
    
        $.post('/cart/remove/', {
            'csrfmiddlewaretoken': csrftoken,
            'id': sku
        }, function (response) {
            /* Hide formset row & change quantity to 0 instead of removing the
            row to preserve the formset in case user POST's a cart update 
            immediately after deleting a row */
            $('tr[data-sku=' + sku + ']').find('.js-quantity').attr('value', '0');
            $('tr[data-sku=' + sku + ']').hide();

            // Update cart values & navbar icon badge
            $('.js-bag-badge').text(response.item_count);
            $('.js-total-item').text('$' + response.item_total.toFixed(2));
            $('.js-total-shipping').text('$' + response.shipping.toFixed(2));
            $('.js-total-order').text('$' + response.order_total.toFixed(2));

            // Show empty cart message if no items left in cart
            if (response.item_total === 0) {
                $('.js-cart-full').hide();
                $('.js-cart-empty').removeClass('hidden');
            }
        });

        return false;
    });

    /* Popup window for product images */
    $('.image-popup').magnificPopup({ 
        type: 'image' 
    });

    /* Swap big image in product template via thumbnail click */
    $('.product-thumbnail').click(function (event) {
        
        var src = $(this).attr('src');

        $('#js-main-image').attr('src', src);
        $('.image-popup').attr('href', src);
    
    });

});

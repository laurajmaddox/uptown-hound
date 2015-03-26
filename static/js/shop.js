$(document).ready(function() {
  
    /* Add navbar shadow on page scroll */
    $(window).scroll(function() {

        if($(this).scrollTop()) {
            $('.navbar').addClass('navbar-shadow');
        } else {
            $('.navbar').removeClass('navbar-shadow');
        }
    
    });

    /* Remove item from cart through Ajax POST */
    $('.js-remove-item').click(function(event) {
    
        var sku = $(event.target).closest('a').data('sku')
    
        $.post('/cart/remove/', {
            'csrfmiddlewaretoken': csrftoken,
            'id': sku
        }, function (response) {
            $('tr[data-sku=' + sku + ']').remove();
            $('.js-bag-badge').text(response.item_count);
            $('.js-total-item').text('$' + response.item_total.toFixed(2));
            $('.js-total-shipping').text('$' + response.shipping.toFixed(2));
            $('.js-total-order').text('$' + response.order_total.toFixed(2));
        });

        return false;
    });

});

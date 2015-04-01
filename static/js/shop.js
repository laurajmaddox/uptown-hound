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

    /* Populate credit card expiration dropdowns in OrderPaymentForm */
    var monthOptions = ['01 - January', '02 - February', '03 - March', '04 - April',
        '05 - May', '06 - June', '07 - July', '08 - August', '09 - September',
        '10 - October', '11 - November', '12 - December']
    for (var i = 0; i < 12; i += 1) {
        $("#js-exp-month").append($("<option></option>").val(i + 1).html(monthOptions[i]));
    }

    var currentYear = new Date().getFullYear()
    for (year = currentYear; year < currentYear + 15; year += 1) {
        $("#js-exp-year").append($("<option></option>").val(year).html(year));
    }

});

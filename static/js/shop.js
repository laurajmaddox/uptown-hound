$(document).ready(function() {
  
    /* Add navbar shadow on page scroll */
    $(window).scroll(function() {

        if($(this).scrollTop()) {
            $('.navbar').addClass('navbar-shadow');
        } else {
            $('.navbar').removeClass('navbar-shadow');
        }
    
    });


    /* Toggle search bar in nav header */
    $('#js-search-toggle').click(function(event) {
        $('#js-nav-search').toggleClass('hidden');
        $('#js-search-toggle').children('span')
            .toggleClass('glyphicon-search')
            .toggleClass('glyphicon-remove');
    });


    /* Remove item from cart through Ajax POST */
    $('.js-remove-item').click(function(event) {
    
        var sku = $(event.target).closest('a').data('sku')
    
        $.post('/cart/remove/', {
            'csrfmiddlewaretoken': csrftoken,
            'id': sku
        }, function (response) {
            $('tr[data-sku=' + sku + ']').find('.js-quantity').attr('value', '0');
            $('tr[data-sku=' + sku + ']').hide();
            $('.js-bag-badge').text(response.item_count);
            $('.js-total-item').text('$' + response.item_total.toFixed(2));
            $('.js-total-shipping').text('$' + response.shipping.toFixed(2));
            $('.js-total-order').text('$' + response.order_total.toFixed(2));
        });

        return false;
    });

    /* Credit card jquery.payment functions */
    $('#js-cc-number').payment('formatCardNumber');
    $('#js-cc-exp').payment('formatCardExpiry');
    $('#js-cc-cvc').payment('formatCardCVC');

    $('.js-checkout-payment').submit(function (event) {
        event.preventDefault();

        $.fn.toggleInputError = function(erred) {
            var errorText = erred ? 
                '<ul class="errorlist">Invalid card info, please check your input.<li></li></ul>' : '';
            this.parent('.form-group').children('.text-danger').html(errorText);
            return this;
        };
        var numVal = $.payment.validateCardNumber($('#js-cc-number').val());
        var expVal = $.payment.validateCardExpiry($('#js-cc-exp').payment('cardExpiryVal'));
        var cvcVal = $.payment.validateCardCVC($('#js-cc-cvc').val(), cardType);

        var cardType = $.payment.cardType($('#js-cc-number').val());
        $('#js-cc-number').toggleInputError(!numVal);
        $('#js-cc-exp').toggleInputError(!expVal);
        $('#js-cc-cvc').toggleInputError(!cvcVal);

        if (numVal && expVal && cvcVal) {
            var expObject = $('#js-cc-exp').payment('cardExpiryVal');
            Stripe.card.createToken({
                number: $('#js-cc-number').val(),
                cvc: $('#js-cc-cvc').val(),
                exp_month: expObject.month,
                exp_year: expObject.year
            }, function (status, response) {
                var $form = $('.js-checkout-payment');
                if (response.error) {
                    console.log(response.error);
                    $form.find('.js-payment-errors').text(response.error.message);
                } else {
                    var token = response.id;
                    $form.append($('<input type="hidden" name="payment-stripe_token" />').val(token));
                    $form.get(0).submit();
                }                
            });
        }
    });

});

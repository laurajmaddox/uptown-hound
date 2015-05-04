/*===============================================
 checkout.js
===============================================*/


$(document).ready(function() {

    // Create Stripe token
    $.createStripeToken = function (cardNum, cvc, expObj) {
        Stripe.card.createToken({
            number: cardNum,
            cvc: cvc,
            exp_month: expObj.month,
            exp_year: expObj.year

        }, function (status, response) {
            var $form = $('.js-checkout-payment');
            
            if (response.error) {                
                $('.js-payment-errors').removeClass('hidden');
                $('.js-payment-errors').text(response.error.message);
                
            } else {
                var token = response.id;

                // Add token as hidden field to form, then submit
                $form.append($('<input type="hidden" name="payment-stripe_token" />').val(token));
                $form.get(0).submit();
            }                           
        });
    };

    // Add or remove form errors in template
    $.fn.toggleInputError = function (erred) {
        var errorText = erred ? 
            '<ul class="errorlist">Invalid card info, please check your input.<li></li></ul>' : '';
        this.parent('.form-group').children('.text-danger').html(errorText);
        return this;
    };

    // jquery.payment field formatting
    $('#js-cc-number').payment('formatCardNumber');
    $('#js-cc-exp').payment('formatCardExpiry');
    $('#js-cc-cvc').payment('formatCardCVC');

    // Validate form data & create token for payment processing
    $('.js-checkout-payment').submit(function (event) {
        
        // Halt form submission
        event.preventDefault();
        // Remove error messages from any previous payment attempt
        $('.js-payment-errors').addClass('hidden');

        Stripe.setPublishableKey('pk_8Oa88NCeR2XVsrIm9uv1qf8QPoEt3');

        var cardType = $.payment.cardType($('#js-cc-number').val());
        var numVal = $.payment.validateCardNumber($('#js-cc-number').val());
        var expVal = $.payment.validateCardExpiry($('#js-cc-exp').payment('cardExpiryVal'));
        var cvcVal = $.payment.validateCardCVC($('#js-cc-cvc').val(), cardType);

        // Toggle errors for valid/invalid input fields
        $('#js-cc-number').toggleInputError(!numVal);
        $('#js-cc-exp').toggleInputError(!expVal);
        $('#js-cc-cvc').toggleInputError(!cvcVal);

        // Create Token if form data is valid
        if (numVal && expVal && cvcVal) {                        
            $.createStripeToken(
                $('#js-cc-number').val(),
                $('#js-cc-cvc').val(),
                $('#js-cc-exp').payment('cardExpiryVal')
            );
        }
    });

});
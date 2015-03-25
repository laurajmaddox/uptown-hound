/*
=================================================
Base template
=================================================
*/

/* Add navbar shadow on page scroll */
$(window).scroll(function() {
    if($(this).scrollTop()) {
        $('.navbar').addClass('navbar-shadow');
    } else {
        $('.navbar').removeClass('navbar-shadow');
    }
});


/*
=================================================
Cart view
=================================================
*/

/* Remove item from session cart */

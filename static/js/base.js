$(window).scroll(function() {
    if($(this).scrollTop()) {
        $('.navbar').addClass('navbar-shadow');
    } else {
        $('.navbar').removeClass('navbar-shadow');
    }
});

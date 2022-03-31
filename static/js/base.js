$(window).scroll(function () {
    if ($(window).scrollTop() >= 50) {
    $('nav').css('background','linear-gradient(to left,#1f212d,#2e2f42)');
    } else {
    $('nav').css('background','transparent');
    }
    });
var loader = $(".loader1");
    var wHeight = $(window).height();
    var wWidth = $(window).width();
    var o = 0;

    loader.css({
        top: wHeight / 2 - 0,
        left: wWidth / 2 - 200
    })

    do {
        loader.animate({
            width: o
        }, 40)
        o += 6;
    } while (o <= 400)
    if (o === 402) {
        loader.animate({
            left: 0,
            width: '100%'
        })
        loader.animate({
            top: '0',
            height: '100%'
        })
    }

    setTimeout(function() {
        $(".loader-wrapper").fadeOut('fast');
        (loader).fadeOut('slow');
    }, 7000);

    $('#fade-in').hide(0).delay(6000).show(1);
    
    //setTimeout(function(){
        //window.location.href = 'anonym';
    // }, 8000);
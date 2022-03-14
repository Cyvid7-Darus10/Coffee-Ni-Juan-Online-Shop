$( ".animation-btn" ).mouseenter(function(e) {
    var parentOffset = $(this).offset(); 

    var relX = e.pageX - parentOffset.left;
    var relY = e.pageY - parentOffset.top;
    $(this).prev(".su_button_circle").css({"left": relX, "top": relY });
    $(this).prev(".su_button_circle").removeClass("desplode-circle");
    $(this).prev(".su_button_circle").addClass("explode-circle");

});

$( ".animation-btn" ).mouseleave(function(e) {
    var parentOffset = $(this).offset(); 
    var relX = e.pageX - parentOffset.left;
    var relY = e.pageY - parentOffset.top;
    $(this).prev(".su_button_circle").css({"left": relX, "top": relY });
    $(this).prev(".su_button_circle").removeClass("explode-circle");
    $(this).prev(".su_button_circle").addClass("desplode-circle");
});

$("#id_email").blur(function() {
    if($(this).val()){
        $("#id_username").addClass("show");
    } else {
        $("#id_username").removeClass("show");
    }
});

$("#id_username").blur(function() {
    if($(this).val()){
        $("#id_first_name").addClass("show");
    } else {
        $("#id_first_name").removeClass("show");
    }
});

$("#id_first_name").blur(function() {
    if($(this).val()){
        $("#id_last_name").addClass("show");
    } else {
        $("#id_last_name").removeClass("show");
    }
});
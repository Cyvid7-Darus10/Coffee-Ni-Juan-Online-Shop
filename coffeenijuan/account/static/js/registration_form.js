if($("#id_username").val()){
    $("#id_username").removeClass("d-none");
}

if($("#id_username").val()){
    $("#id_username").removeClass("d-none");
}

if($("#id_first_name").val()){
    $("#id_first_name").removeClass("d-none");
}

if($("#id_last_name").val()){
    $("#id_last_name").removeClass("d-none");
    $(".container").removeClass("py-5");
}

$("#id_email").blur(function() {
    if($(this).val()){
        $("#id_username").removeClass("d-none");
    } else {
        $("#id_username").addClass("d-none");
    }
});

$("#id_username").blur(function() {
    if($(this).val()){
        $("#id_first_name").removeClass("d-none");
        $(".container div.row").removeClass("py-5");
        $(".container div.row").addClass("py-2");
    } else {
        $("#id_first_name").addClass("d-none");
    }
});

$("#id_first_name").blur(function() {
    if($(this).val()){
        $("#id_last_name").removeClass("d-none");
        $(".container").removeClass("py-5");
    } else {
        $("#id_last_name").addClass("d-none");
        $(".container").addClass("py-5")
    }
});
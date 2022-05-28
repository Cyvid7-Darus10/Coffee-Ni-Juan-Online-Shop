$(document).ready(function(){ 
  $('#payment_method').on("change", function() {

      var opval = $(this).val(); 

      $(".payment_option_input").prop("value", opval);

      if(opval=="online"){ 
        $('#onlinePayment').modal("show");
      }else if(opval=="bank"){ 
        $('#bankTransfer').modal("show"); 
      }
  });

  $(".confirm_submit").on("click", function() {
    $('.submit_payment_form').trigger("click");
  })

  $('.place_order').on("click", function() { 
      var opval = $("#payment_method").val(); 
      if(opval=="Select"){ 
        $('#noPaymentOption').modal("show"); 
      } else {
        $('#defaultModal').modal("show"); 
      }
  });

  $("#save_file1, #save_file2").on("click", function() {
    let mainInput = $("#proof");
    let id;
    if(this.id =="save_file1")
      id = "file1";
    else if(this.id =="save_file2")
      id = "file2";

    let secondaryInput = $("#"+id);
    let copy1 = mainInput.clone()
    let copy2 = secondaryInput.clone()

    if(mainInput.val()!=secondaryInput.val()) {
      mainInput.after(copy2)
      mainInput.remove()
      secondaryInput.after(copy1)
      secondaryInput.remove()

      $("#proof").attr("id", "temp");
      $("#"+id).attr("id", "proof");
      $("#temp").attr("id", id);

      $("#"+id).css("display", "inline");
      // $("#proof").css("display", "none");
    }
  })
});
$(document).ready(function(){ 
  $('#payment_method').on("change", function() {

      var opval = $(this).val(); 

      $(".payment_option_input").prop("value", opval);

      let shipping_fee_price = parseInt($(".shipping_fee_price").text());
      let total_price = parseInt($(".total_price").text());

      console.log($(".total_price").text());

      if(opval=="cod") {
        if(!($(".shipping_fee").length))
          $('.grand_total').append(`<span class="shipping_fee"> + Shipping Fee (₱${shipping_fee_price}) = ₱${shipping_fee_price + total_price}</span>`).hide().fadeIn(300)
        else
          $(".shipping_fee").fadeIn(300)
      } else {
        if($(".shipping_fee").length)
          $(".shipping_fee").fadeOut(300)
      }

      // if(opval=="online"){ 
      //   $('#onlinePayment').modal("show");
      // }else if(opval=="bank"){ 
      //   $('#bankTransfer').modal("show"); 
      // }else{
      //   $("#proof_exist").prop("value", "None");
      // }
      //   console.log($("#proof").prop("value"));
  });

  $(".confirm_submit").on("click", function() {
      // if ($("#proof_exist").prop("value") != "None"){
      //   $("#proof_exist").prop("value", "Not None");
      // }else{
      //   $("#proof_exist").prop("value", "None");
      // }
    $('.submit_payment_form').trigger("click");
  })

  $('.place_order').on("click", function() { 
      let opval = $("#payment_method").val(); 
      // console.log(opval)
      let len = $(".product").length;

      if(len == 0) {
        $('#noProduct').modal("show"); 
      } else if(opval=="select"){ 
        $('#noPaymentOption').modal("show"); 
      } else {
        $('#defaultModal').modal("show"); 
      }
  });

  // $("#save_file1, #save_file2").on("click", function() {
  //   let mainInput = $("#proof");
  //   let id;
  //   if(this.id =="save_file1")
  //     id = "file1";
  //   else if(this.id =="save_file2")
  //     id = "file2";

  //   let secondaryInput = $("#"+id);
  //   let copy1 = mainInput.clone()
  //   let copy2 = secondaryInput.clone()

  //   if(mainInput.val()!=secondaryInput.val()) {
  //     mainInput.after(copy2)
  //     mainInput.remove()
  //     secondaryInput.after(copy1)
  //     secondaryInput.remove()

  //     $("#proof").attr("id", "temp");
  //     $("#"+id).attr("id", "proof");
  //     $("#temp").attr("id", id);

  //     $("#"+id).css("display", "inline");
  //     $("#proof").css("display", "none");
  //   }
  // })
});
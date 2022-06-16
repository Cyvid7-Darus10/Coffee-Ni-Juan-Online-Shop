$(document).ready(function(){ 
  $('#payment_method').on("change", function() {

      var opval = $(this).val(); 

      $(".payment_option_input").prop("value", opval);

      let shipping_fee_price = parseInt($(".shipping_fee_price").text());
      let total_price = parseInt($(".total_price").text());


      if(opval=="cod") {
        if(!($(".shipping_fee").length))
          $('.grand_total').append(`<span class="shipping_fee"> + Shipping Fee (₱${shipping_fee_price}) = ₱${shipping_fee_price + total_price}</span>`).hide().fadeIn(300)
        else
          $(".shipping_fee").fadeIn(300)
      } else {
        if($(".shipping_fee").length)
          $(".shipping_fee").fadeOut(300)
      }

    $('.submit_payment_form').trigger("click");
  })

  $('.place_order').on("click", function() { 
      let opval = $("#payment_method").val(); 
      let len = $(".product").length;

      if(len == 0) {
        $('#noProduct').modal("show"); 
      } else if(opval=="select"){ 
        $('#noPaymentOption').modal("show"); 
      } else {
        $('#defaultModal').modal("show"); 
      }
  });
});
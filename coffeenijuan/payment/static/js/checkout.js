$(document).ready(function(){ 
  $('#payment_method').on("change", function() { 
      var opval = $(this).val(); 
      if(opval=="online"){ 
        $('#onlinePayment').modal("show");
      }else if(opval=="bank"){ 
        $('#bankTransfer').modal("show"); 
      }
  });
$('.place_order').on("click", function() { 
      var opval = $("#payment_method").val(); 
      if(opval=="Select"){ 
        $('#noPaymentOption').modal("show"); 
      } else {
        $('#defaultModal').modal("show"); 
      }
  });
});


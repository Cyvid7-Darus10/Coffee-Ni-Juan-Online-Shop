$(document).ready(function(){ 
  $('#payment_method').change(function() { 
      var opval = $(this).val(); 
      if(opval=="online"){ 
          $('#onlinePayment').modal("show"); 
      }else if(opval=="bank"){ 
        $('#bankTransfer').modal("show"); 
      }
  });
});


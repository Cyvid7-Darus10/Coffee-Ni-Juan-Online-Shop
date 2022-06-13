$(document).ready(function() {
	$('#select-all').click(function() {
	  var checked = this.checked;
	  $('input[type="checkbox"]').each(function() {
		this.checked = checked;
	  });
	})


	// $('#check_out_form').on("submit", function(e) {
      //   $.ajaxSetup({
      //       headers: {
      //           "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
      //       }
      //   });


      //   $.ajax({
	     //    url: `{% url payment:check_out %}`,
	     //    method: 'POST',
	     //    data: $(this).serialize(),
	     //    dataType: 'json',
	     //    success: function (data) {
	     //    	console.log("Success");
      //   	}
      // });
	//     e.preventDefault();
	// });

	let checkedItems = $(".checkItem");
	let products = $(".single-product");

	products.each(function(i, obj) {
		let checked = $(this).find(".checkItem").is(":checked");
		let totalPrice = $(this).find(".totalPrice").text();
		let quantity = $(this).find(".quantity").text();
		let price = $(this).find(".price").text();
		let productId = $(this).find(".productId").html();
		if(checked)
			$(".prices").append(`<span id="itemSummary${productId}" class="itemSummary clearfix">₱ <span class="price">${price}</span> x <span class="quantity">${quantity}</span> = ₱ <span class="totalPrice">${totalPrice}</span></span>`)
		else
			$(".prices").append(`<span id="itemSummary${productId}" class="itemSummary clearfix" hidden>₱ <span class="price">${price}</span> x <span class="quantity">${quantity}</span> = ₱ <span class="totalPrice">${totalPrice}</span></span>`)
		console.log(`itemSummary${productId}`)
		// console.log($(this).find(".totalPrice").text())
		// console.log(checked);
	});

	$(".selectAll").on("change", function() {
		let checked = $(this).is(":checked");
		if(!checked) {
			$(".itemSummary").fadeOut(300)
		} else if(checked) {
			$(".itemSummary").fadeIn(300)
		}
		getGrandTotal();
	})

	$(".checkItem").on("change", function() {
		let checked = $(this).is(":checked");
		let priceSummary = $(".prices");
		let productId = $(this).closest('div').find(".productId").html();
		if(!checked) {
			priceSummary.find("#itemSummary"+productId).fadeOut(300)
		} else if(checked) {
			priceSummary.find("#itemSummary"+productId).fadeIn(300)
		}
		getGrandTotal();
	})

	$(".qty").on("keyup", function() {
		let newValue = $(this).val()
		let price = $(this).closest('div').find(".price").text();
		let productId = $(this).closest('div').find(".productId").html();
		console.log("Hello")
		console.log(price)
		$(this).closest('div').find(".quantity").text(newValue.toString())
		$(this).closest('div').find(".totalPrice").text((parseInt(price)*newValue).toString())

		$(`#itemSummary${productId}`).find(".quantity").text(newValue.toString())
		$(`#itemSummary${productId}`).find(".totalPrice").text((parseInt(price)*newValue).toString())
		getGrandTotal();
	})

	function getGrandTotal() {
		let products = $(".single-product");
		let total = 0;
		products.each(function(i, obj) {
			let checked = $(this).find(".checkItem").is(":checked");
			let totalPrice = $(this).find(".totalPrice").text();
			if(checked)
				total+=parseFloat(totalPrice);
		});
		$(".grandTotal").text(total.toString());
	}

	// for(let i = 0; i < checkedItems.length; i++) {
	// 	let productPrice = 0;

	// }
});
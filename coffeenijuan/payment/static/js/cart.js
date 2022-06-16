window.addEventListener( "pageshow", function ( event ) {
	var historyTraversal = event.persisted || 
						   ( typeof window.performance != "undefined" && 
								window.performance.navigation.type === 2 );
	if ( historyTraversal ) {
	  // Handle page restore.
	  window.location.reload();
	}
});

$(document).ready(function() {
	$('#select-all').click(function() {
	  var checked = this.checked;
	  $('input[type="checkbox"]').each(function() {
		this.checked = checked;
	  });
	})

	let products = $(".single-product");

	products.each(function(i, obj) {
		let checked = $(this).find(".checkItem").is(":checked");
		let total_price = $(this).find(".totalPrice").text();
		let quantity = $(this).find(".quantity").text();
		let price = $(this).find(".price").text();
		let product_id = $(this).find(".productId").html();
		if(checked) {
			$(".prices").append(`<span id="itemSummary${product_id}" class="itemSummary clearfix">₱ <span class="price">${price}</span> x <span class="quantity">${quantity}</span> = ₱ <span class="totalPrice">${total_price}</span></span>`)
		}
		else {
			$(".prices").append(`<span id="itemSummary${product_id}" class="itemSummary clearfix">₱ <span class="price">${price}</span> x <span class="quantity">${quantity}</span> = ₱ <span class="totalPrice">${total_price}</span></span>`)
			$(`#itemSummary${product_id}`).hide()			
		}
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
		let price_summary = $(".prices");
		let product_id = $(this).closest('div').find(".productId").html();
		console.log(price_summary.find("#itemSummary"+product_id));

		if(!checked) {
			price_summary.find("#itemSummary"+product_id).fadeOut(300)
		} else {
			price_summary.find("#itemSummary"+product_id).fadeIn(300)
		}
		getGrandTotal();
	})

	$(".qty").on("keyup", function() {
		let new_value = $(this).val()
		let price = $(this).closest('div').parent().find(".price").text();
		let product_id = $(this).closest('div').find(".productId").html();
		$(this).closest('div').parent().find(".quantity").text(new_value.toString())
		$(this).closest('div').parent().find(".totalPrice").text((parseInt(price)*new_value).toString())

		console.log(new_value);

		$(`#itemSummary${product_id}`).find(".quantity").text(new_value.toString())
		$(`#itemSummary${product_id}`).find(".totalPrice").text((parseInt(price)*new_value).toString())
		getGrandTotal();
	})

	function getGrandTotal() {
		let products = $(".single-product");
		let total = 0;
		products.each(function(i, obj) {
			let checked = $(this).find(".checkItem").is(":checked");
			let total_price = $(this).find(".totalPrice").text();
			if(checked)
				total+=parseFloat(total_price);
		});
		$(".grandTotal").text(total.toString());
	}
});
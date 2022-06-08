// $(".productTitle").text("Hello");

$(".plus").on("click", function() {
	let val = parseInt($(".qty").val());
	if (val < parseInt($("#stock").text())) {
		$(".qty").val(val + 1);
	}
});

$(".minus").on("click", function() {
	let val = parseInt($(".qty").val());
	if (val > 1) {
		$(".qty").val(val - 1);
	}
});

$(".qty").on("keyup keydown", function() {
	let val = parseInt($(".qty").val());
	console.log(val)
	let stock = parseInt($("#stock").text());
	if($(".qty").val() == "") {
		$(".qty").val(0);		
	}
	if(val > stock || !(/^([0-9])+$/.test($(".qty").val()))) {
		$(".qty").val(stock);
	}
})
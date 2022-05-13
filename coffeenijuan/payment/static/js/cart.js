$(".plus").on("click", function() {
	let val = parseInt($(".qty").val());
	$(".qty").val(val + 1);
});

$(".minus").on("click", function() {
	console.log("GASDSA")
	let val = parseInt($(".qty").val());

	if (val > 1) {
		$(".qty").val(val - 1);
	}
});
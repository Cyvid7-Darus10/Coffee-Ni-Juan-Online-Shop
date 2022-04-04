// $(".productTitle").text("Hello");

$(".amount").val(0);

$(".plus").on("click", function() {
	let val = parseInt($(".amount").val());
	$(".amount").val(val+1);
});

$(".minus").on("click", function() {
	let val = parseInt($(".amount").val());
	if(val>0)
		$(".amount").val(val-1);
});

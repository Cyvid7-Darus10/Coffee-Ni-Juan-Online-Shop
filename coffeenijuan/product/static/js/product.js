// $(".productTitle").text("Hello");

$(".plus").on("click", function() {
	let val = parseInt($("#quantity").val());
	if (val < parseInt($(".stock").text())) {
		$("#quantity").val(val + 1);
	}
});

$(".minus").on("click", function() {
	let val = parseInt($("#quantity").val());
	if (val > 1) {
		$("#quantity").val(val - 1);
	}
});

$(".qty").on("keyup keydown", function() {
	let $this = $(this);
	let val = parseInt($this.val());
	let stock = parseInt($this.closest("div").find(".stock").text());
	if($this.val() == "" || /^(0[0-9]*)+$/.test($(".qty").val())) {
		$this.val(1);
	}
	if(val > stock || !(/^([0-9])+$/.test($(".qty").val()))) {
		$this.val(stock);
	}
})
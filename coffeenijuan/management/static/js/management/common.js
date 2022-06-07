$(".confirm-btn").click(function() {
    let label = $(this).attr('data-label');
    let url = $(this).attr('data-url');

    $("#staticBackdrop .modal-title").html(`Confirmation to Delete`);
    $("#staticBackdrop .modal-body").html(`Are you sure you want to delete, ${label}?`);
    $("#staticBackdrop .modal-footer .btn-primary").attr('href', url);
    $('#staticBackdrop').modal('show');
});
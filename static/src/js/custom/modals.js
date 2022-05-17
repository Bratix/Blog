$(function(){
    $(".delete_blog_trigger").on("click", function () { 
        let deleteModalID = $(this).attr("data-tw-target");
        cash(deleteModalID).modal("show");
    });

    $("#cancel_action_trigger").on("click", function () { 
        console.log('action starting');
        let modalId = $(this).attr("data-tw-target");
        cash(modalId).modal("show");
    });

    $(document).on("click", ".post_delete_modal", function () { 
        let deleteModalID = $(this).attr("data-tw-target");
        console.log(deleteModalID);
        cash(deleteModalID).modal("show");
    });
})
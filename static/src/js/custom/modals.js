$(document).ready(function(){
    $(".delete_modal").on("click", function () { 
        let deleteModalID = $(this).attr("data-modal")
        cash("#"+deleteModalID).modal("show");
    });

    $("#cancel_action_trigger").on("click", function () { 
        console.log('action starting')
        let modalId = $(this).attr("data-tw-target")
        cash(modalId).modal("show");
    });
})
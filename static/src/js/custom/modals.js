$(function(){
    $(document).on("click", ".modal_trigger", function () { 
        let deleteModalID = $(this).attr("data-tw-target");
        cash("#" + deleteModalID).modal("show");
    });
})
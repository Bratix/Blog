
$(function(){
    if($("#image_input").hasClass("has-error")){
        $(".file-upload-border").addClass("has-error");
    }

    $("#image_input").on('change', function(){
        var file = $('#image_input')[0].files[0].name;
        $(".file-name").text(file);
    })
})

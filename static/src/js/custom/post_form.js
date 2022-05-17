
$(function(){
    
    
    
    $("#post_form_submit").on('click', function(e){
        e.preventDefault();
        $("#post_form").trigger('submit');
    })

    if($("#post_image").hasClass("has-error")){
        $(".file-upload-border").addClass("has-error");
    }

    $("#post_image").on('change', function(){
        var file = $('#post_image')[0].files[0].name;
        $(".file-name").text(file);
    })

})

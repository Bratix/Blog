$(document).ready(function(){
    $(".comment-form").on('submit',function(e){
        e.preventDefault();
        
        var text = $('#id_comment_text').val()
        var url = $(this).data("action")
        var token = $("input[name='csrfmiddlewaretoken']").val()
        
        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            dataType: "json",
            url: url,
            data: {
                comment_text: text,
            },
        }).done(function(){
            $('#id_comment_text').val("")
            console.log(pk)
        });
    })
        
})
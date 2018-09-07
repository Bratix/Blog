$(document).ready(function(){

    $(".comment-form").submit(function(e){
        e.preventDefault()
        e.stopImmediatePropagation()

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
        }).done(function(data){
            $('#id_comment_text').val("")
            $('#comment-count').text(data.comment_count)
            $('.comment-count-main').text(data.comment_count+ " comments")
            $('#comment-count-hidden').attr('value', data.comment_count)
            $(".refresh-list").load(location.href + " .refresh-list")
        });
    });
})
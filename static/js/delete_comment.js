$(document).ready(function(){
  
    var comment_count = $("#comment-count").text()
    for(i = 1; i <= comment_count; i++){
        $("#comment-delete-"+i).submit(function(e){
            e.preventDefault()
            var url = $(this).data("action_delete")
            var id = $(this).data("value")
            var token = $("input[name='csrfmiddlewaretoken']").val()
            var current_comment_count = $("#comment-count").text()

            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": token,
                },
                url: url,
            }).done(function(){
                $('#'+id+'-object').remove()
                $('#comment-count').html(current_comment_count-1)
                $('.comment-count-main').html(current_comment_count-1 + " comments") 
            });
        });
    }

})




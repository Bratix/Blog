$(document).ready(function(){
    $(".like_button").click(function(e){
        e.preventDefault()
        var url = $(this).data("href")
        var token = $("input[name='csrfmiddlewaretoken']").val()
        console.log(token);
        
        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
            dataType: "json",

            }).done(function(data){
            $("#like-counter").html(" " + data.like_counter)
            
            if(data.user_like === true)
            {
            $(".liked").removeClass(".glyphicon glyphicon-heart-empty")
            $(".liked").addClass(".glyphicon glyphicon-heart")}
            
            else
            {
            $(".liked").removeClass(".glyphicon glyphicon-heart")
            $(".liked").addClass(".glyphicon glyphicon-heart-empty")
            }
        });
    })
})

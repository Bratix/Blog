$(document).ready(function(){
    $(".like_button").click(function(e){
        e.preventDefault()
        var url = $(this).data("href")
        var token = $("input[name='csrfmiddlewaretoken']").val()
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
            $(".liked").removeClass(".fa fa-heart-o")
            $(".liked").addClass(".fa fa-heart")}
            
            else
            {
            $(".liked").removeClass(".fa fa-heart")
            $(".liked").addClass(".fa fa-heart-o")
            }
        });
    })
})

$(document).ready(function(){
    $(".like_button").click(function(e){
        e.preventDefault()
        console.log("like.clicked")
        var url = $(this).data("href")
        var token = $("input[name='csrfmiddlewaretoken']").val()
        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
            dataType: "json",

            }).done(function() {
            console.log()
            $("#like-counter").html(" " + like_counter)
            if(user_like === true)
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

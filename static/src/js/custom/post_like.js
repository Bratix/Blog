$(function(){
    $(".like_button").on('click', function(e){
        e.preventDefault();
        $(this).hide();
        var url = $(this).data("href");
        var token = $("input[name='csrfmiddlewaretoken']").val();
        console.log(token)
        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
            dataType: "json",

            }).done(function(data){
            $("#like-counter").html(" " + data.like_counter)
            
            if(data.user_like === true){
            $(".liked").removeClass("bi-heart")
            $(".liked").addClass("bi-heart-fill")
            } else{
            $(".liked").removeClass("bi-heart-fill")
            $(".liked").addClass("bi-heart")
            }

            $(".like_button").fadeIn(400)
        });
    })
})

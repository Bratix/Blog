$(document).ready(function(){
    $(".like_button").click(function(e){
        e.preventDefault()
        console.log("like.clicked")
        var url = $(this).data("href")
        var token = $("input[name='csrfmiddlewaretoken']").val()
        $.ajax({
            type: "POST",
            url: url,
            token: token,
            csrfmiddlewaretoken: token,
            headers: {
                "X-CSRFToken": token,
            }
            }).done(function(response) {
            console.log(response)
            $("#like-counter").html("10")
            });
    })
})
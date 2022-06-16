$(function(){
    $('.friend_request_action').on('click', function(e){

        var url = $(this).data("href");
        let show = $(this).data("show");
        var token = $("input[name='csrfmiddlewaretoken']").val();
        let request_options_buttons = $(this).closest('.request_options')
        $.ajax({
            type: "POST",
            dataType: "json",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
        }).done(function(data){
            request_options_buttons.hide(300)
            $("#" + show).fadeIn(300)
        })
    })

    $('.add-remove-friend').on('click', function(e){

        var url = $(this).data("href");
        var token = $("input[name='csrfmiddlewaretoken']").val();
        let request_options_buttons = $(this).closest('.request_options')
        $.ajax({
            type: "POST",
            dataType: "json",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
        }).done(function(data){
            if (data.success = 'failed'){
                request_options_buttons.hide()
                $("#success_note").html(data.message).fadeIn(300)
            }
                
            request_options_buttons.hide()
            $("#success_note").fadeIn(300)
        })
    })

})
$(function(){
    $('#subscription_toggle').on('click', function(e){
        e.preventDefault();

        var url = $(this).data("href");
        $.ajax({
            type: "GET",
            dataType: "json",
            crossDomain:true,
            url: url,
        }).done(function(data){
            if (data.status === 'unsubbed'){
                $('#subscription_toggle').fadeOut(300).removeClass('btn-rounded-danger').addClass('btn-rounded-primary').html('Subscribe').fadeIn(300)
            } else if (data.status === 'subbed'){
                $('#subscription_toggle').fadeOut(300).removeClass('btn-rounded-primary').addClass('btn-rounded-danger').html('Unsubscribe').fadeIn(300)
            }

            $("#subscribers").fadeOut(100)
            $("#subscribers").fadeIn(100).html(data.subscribers)
        })
    })
})
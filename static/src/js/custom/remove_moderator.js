import 'waypoints/lib/jquery.waypoints.min.js';
import 'waypoints/lib/shortcuts/infinite.min.js';


$(function(){
    $(".remove-moderator").on("click", function () { 
        var url = $(this).data("href");
        var token = $("input[name='csrfmiddlewaretoken']").val();
        let hide = $(this).data("hide")
        $.ajax({
            crossDomain:true,
            type: "POST",
            dataType: "json",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
        }).done(function(data){
            $("#" + hide).removeClass("intro-x").fadeOut(500)
        })
    });
    
})

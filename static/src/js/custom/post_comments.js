import Toastify from "toastify-js";
import 'waypoints/lib/jquery.waypoints.min.js';
import 'waypoints/lib/shortcuts/infinite.min.js';

$(function(){


    $("#comment-form").on('submit' ,function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        
        var text = $('#comment_text').val();
        
        if(text===" " || text===""){
            $("#comment_form_notification").trigger('click');
            return
        }

        var url = $(this).data("action");
        console.log(url)
        var token = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            dataType: "json",
            url: url,
            data: {
                text: text,
            },
        }).done(function(data){

            $('#comment_text').val("");
            $('.comment-count').hide();
            $('.comment-count').text(data.comment_count).fadeIn(1000);
            console.log(data);

            let comment = generate_comment(data)
            
            $("#comment-list").prepend(comment);

            Waypoint.refreshAll();
        });
    });


    $(document).on('click', '.comment_edit_link', function(e) {
        e.preventDefault();

        let target = $(this).attr('data-update-form')
        let comment_main = $(this).attr('data-hide')
        console.log("#" + target)
        $("#" + comment_main).hide();
        $("#" + target).fadeIn(500);   
                
    });

    $(document).on('submit', '.comment-update-form', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();

        var url = $(this).data("action");
        let comment_main = $("#" + $(this).attr('data-show'))
        let form = $(this)
        console.log(url)
        var token = $("input[name='csrfmiddlewaretoken']").val();

        var text = $(this).find('#comment_text').val();
        console.log(text)
        if(text===" " || text===""){
            $("#comment_form_notification").trigger('click');
            return
        }

        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
            data: {
                text: text,
            },
        }).done(function(data){
            
            comment_main.find("#edited").html("edited");
            comment_main.find("#text").html(data.text);
            comment_main.find("#date").html(data.creation_date);

            form.hide();
            comment_main.fadeIn(500)
        })
    })

    
    $(document).on('submit', '.comment_delete_form' ,function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var url = $(this).attr("action");
        console.log(url)
        var token = $("input[name='csrfmiddlewaretoken']").val();
        var current_comment_count = $(".comment-count:first").text();
        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            url: url,
        }).done(function(){
            $('.comment-count').hide();
            $('.comment-count').html(current_comment_count-1).fadeIn(400);
        })
        
        let div = $(this).data("div");
        console.log(div)
        $('#' + div).fadeOut(400);
        setTimeout(() => {
            $('#' + div).remove;
            Waypoint.refreshAll();
        }, 500)

        let page_query_param = $('.infinite-more-link').attr('href')
        const params = new Proxy(new URLSearchParams(page_query_param), {
            get: (searchParams, prop) => searchParams.get(prop),
        });       
    });

    $("#comment_form_notification").on("click", function() {
        Toastify({
            node: $("#basic-non-sticky-notification-content")
                .clone()
                .removeClass("hidden")[0],
            duration: 5000,
            newWindow: true,
            close: true,
            gravity: "top",
            position: "right",
            backgroundColor: "white",
            stopOnFocus: true,
        }).showToast();
    });
})

    
function generate_comment(data) { 
    let comment = $("#empty-comment").clone().removeClass("hidden").attr('id','comment-'+data.pk);
    comment.find("#date").html(data.creation_date);
    comment.find("#user").html(data.user);
    comment.find("#text").html(data.text);

    let new_id = "comment_delete_" + data.pk;
    comment.find("#delete_toggle").attr('data-tw-target', new_id);
    comment.find("#delete_toggle").attr('id', '');
    comment.find("#comment_delete").attr('id', 'comment_delete_' + data.pk);
    comment.find(".comment_delete_form").attr('action', data.delete_link)

    let div_id = 'comment-' + data.pk;
    comment.find(".comment_delete_form").attr('data-div', div_id);

    let comment_main = 'comment-main-' + data.pk
    comment.find("#comment_main").attr('id', comment_main);
    
    let comment_update_form = 'comment-update-form-'+ data.pk;
    comment.find("#edit_toggle").attr('data-update-form', comment_update_form)
    
    comment.find("#edit_toggle").attr('data-hide', comment_main)

    comment.find(".comment-update-form").attr('id', comment_update_form);
    comment.find(".comment-update-form").attr('data-action', data.update_link)
    comment.find(".comment-update-form").attr('data-show', comment_main)
    comment.find("#comment_text").html(data.text)
    
    return comment
}
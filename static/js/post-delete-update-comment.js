//post comment
$(document).ready(function(){

    $(".comment-form").submit(function(e){
        e.preventDefault()
        e.stopImmediatePropagation()

        var text = $('#id_comment_text').val()
        var url = $(this).data("action")
        var token = $("input[name='csrfmiddlewaretoken']").val()
        
        $.ajax({
            type: "POST",
            headers: {
                "X-CSRFToken": token,
            },
            dataType: "json",
            url: url,
            data: {
                comment_text: text,
            },
        }).done(function(data){

            var monthNames = [
                "JAN", "FEB", "MAR",
                "APR", "MAY", "JUN", "JUL",
                "AUG", "SEP", "OCT",
                "NOV", "DEC"
              ];

            var date = new Date(data.creation_date);
            $('#id_comment_text').val("")
            $('#comment-count').text(data.comment_count)
            $('.comment-count-main').text(data.comment_count+ " comments")

            var Com = $("#emptycom").clone().removeClass("hidden").attr('id','').fadeIn(600)
            Com.find("#comdate").html(date.getDate()+" "+monthNames[date.getMonth()]+" "+ date.getFullYear()+" at "+('0'+date.getHours()).slice(-2)+":"+('0'+date.getMinutes()).slice(-2))
            Com.find("#comuser").html(data.user)   
            Com.find("#comtext").html(data.comment_text)
            var durl = Com.find(".btn-cdelete").data('url');
            url_delete = durl.substring(0, durl.length-1)+data.pk
            Com.find(".btn-cdelete").data("url",url_delete)
            Com.find("#comment_text").val(data.comment_text)
            var uurl = Com.find('.update-com').data("url").split("/")
            url_update ='/'+uurl[1]+'/'+data.pk+'/'+uurl[3]
            Com.find('.update-com').data("url",url_update)
            Com.find('.update-com').attr("data-url",url_update)

            $(".comment-list").append(Com)

            
        });
    });
})

//Update comment
$(document).ready(function(){

    $(".comment-list").on('click','.btn-cupdate',function(){
        $(this).closest('li').find('.comment-text-update').removeClass('hidden')
        $(this).closest('li').find('#comtext').addClass('hidden')
        var token = $("input[name='csrfmiddlewaretoken']").val()

        $(".comment-list").on('click','.update-com',function(e){
            uurl = $(this).data('url')
            
            comment_text = $(this).closest('div').find('.form-control').val()
            var token = $("input[name='csrfmiddlewaretoken']").val()
            
            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": token,
                },
                url: uurl,
                data: {
                    comment_text: comment_text,
                },
            })
            
            $(this).closest('li').find('#comtext').html(comment_text).removeClass('hidden')
            $(this).closest('li').find('.comment-text-update').addClass('hidden')
        })
        
        
    });

});

//delete comment
$(document).ready(function(){

        $(".comment-list").on('click','.btn-cdelete',function(){
            var url = $(this).data("url")
            var token = $("input[name='csrfmiddlewaretoken']").val()
            var current_comment_count = $("#comment-count").text()
            $.ajax({
                type: "POST",
                headers: {
                    "X-CSRFToken": token,
                },
                url: url,
            }).done(function(){
                $('#comment-count').html(current_comment_count-1)
                $('.comment-count-main').html(current_comment_count-1 + " comments") 
            })
            $(this).closest('li').fadeOut(600)
        });
    
});
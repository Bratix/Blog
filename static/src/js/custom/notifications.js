function newNotification(notification, pk) {
    let html_notification
    let date = new Date(notification.created_at);

    if (notification.url.includes('chat') && notification.url === window.location.pathname){
        let url = ajax_url + "notification/delete/" + pk
        
        var token = $("input[name='csrfmiddlewaretoken']").val();
        
        let settings = {
            url: url,
            method: "POST",
            timeout: 0,
            headers: {
                "X-CSRFToken": token,
            },
        };
        $.ajax(settings).done(function (response) {
        });

        return
    }

    if ($('#notification-' + pk).length > 0) {
        html_notification = $('#notification-' + pk)
    } else {
        html_notification = $("#empty-notification").clone().removeClass("hidden").attr('id',"notification-" + pk);
    }

    html_notification.find("#created_at").html(date.toLocaleString());
    html_notification.find("#profile-pic").attr('src', notification.thumb_image);
    html_notification.find("#title").html(notification.title);
    html_notification.find("#title").attr('href', notification.url);
    html_notification.find("#text").html(notification.text);
    
    return html_notification
}

async function getNotifications(){
    let url = ajax_url + "notifications"
    let settings = {
        url: url,
        method: "GET",
        timeout: 0
    };
    let last_timestamp
    await $.ajax(settings).done(function (response) {
        response.forEach( element => {
            last_timestamp = element.fields.created_at
            let notification = newNotification(element.fields, element.pk)
            $("#notifications").after(notification)
        });

        if (response.length > 0){
            $("#notification-dropdown").addClass('notification--bullet')
        }
    });
    return last_timestamp
}

async function getNotificationsFeed(last_timestamp){
    let url = ajax_url + "notifications/new/" + last_timestamp
    let settings = {
        url: url,
        method: "GET",
        timeout: 0,
    };
    await $.ajax(settings).done(function (response) {
        if (response.length > 0) {
            response.forEach( element => {
                last_timestamp = element.fields.created_at
                let notification = newNotification(element.fields, element.pk)
                $("#notifications").after(notification)
            });

            $("#notification-dropdown").addClass('notification--bullet')
                        
        }                
    });
    return last_timestamp
}



async function delay(ms) {
    return await new Promise(resolve => setTimeout(resolve, ms));
}
  

async function notificationListener(){
    let last_timestamp = await getNotifications()
    await delay(1000);

    if (last_timestamp == undefined){
        let date = new Date();
        last_timestamp = date.toISOString()
    }
    
    while (true) {
        last_timestamp = await getNotificationsFeed(last_timestamp);
        await delay(1000);
    }
} 


$(function(){
    $(document).on('click', '.notification-thumb', function(){
        let url = $(this).find("#title").attr('href')
        window.location.pathname = url
    })

    $("#notification-dropdown").on('click', function(){
        $(this).removeClass('notification--bullet')
    })

    if ($("#notification-dropdown").length > 0){
        notificationListener()
    }
})
  

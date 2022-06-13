function newNotification(notification, pk) {
    console.log(notification)
    let html_notification
    let date = new Date(notification.created_at);

    if (notification.url.includes('chat') && notification.url === window.location.pathname){
        let url = "http://localhost:8000/notification/delete/" + pk
        var token = $("input[name='csrfmiddlewaretoken']").val();
        
        let settings = {
            "url": url,
            "method": "POST",
            "timeout": 0,
            headers: {
                "X-CSRFToken": token,
            },
        };
        $.ajax(settings).done(function (response) {
            console.log(response)
        });

        return
    }

    if ($('#notification-' + pk).length > 0) {
        console.log('#notification' + pk)
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
    let url = "http://localhost:8000/notifications"
    let settings = {
        "url": url,
        "method": "GET",
        "timeout": 0
    };
    let last_timestamp
    await $.ajax(settings).done(function (response) {
        response.forEach( element => {
            last_timestamp = element.fields.created_at
            let notification = newNotification(element.fields, element.pk)
            $("#notifications").after(notification)
        });
    });
    return last_timestamp
}

async function getNotificationsFeed(last_timestamp){
    let url = "http://localhost:8000/notifications/new/" + last_timestamp
    let settings = {
        "url": url,
        "method": "GET",
        "timeout": 0,
    };
    await $.ajax(settings).done(function (response) {
        if (response.length > 0) {
            response.forEach( element => {
                last_timestamp = element.fields.created_at
                let notification = newNotification(element.fields, element.pk)
                $("#notifications").after(notification)
            });
        }                
    });
    return last_timestamp
}



async function delay(ms) {
    return await new Promise(resolve => setTimeout(resolve, ms));
}
  

async function chartListener(){
    let last_timestamp = await getNotifications()
    await delay(1000);

    if (last_timestamp == undefined){
        let date = new Date();
        last_timestamp = date.toISOString()
    }
    console.log(last_timestamp)
    while (true) {
        last_timestamp = await getNotificationsFeed(last_timestamp);
        console.log(last_timestamp)
        await delay(1000);
    }
} 


$(function(){
    $(document).on('click', '.notification-thumb', function(){
        console.log(this)
        let url = $(this).find("#title").attr('href')
        window.location.pathname = url
    })

    chartListener()
})
  

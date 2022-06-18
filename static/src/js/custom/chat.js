$(function(){
       
    let url = window.location.href
    if (url.includes('chat')){
        const chat_id = JSON.parse(document.getElementById('chat_id').textContent);
        const user_id = JSON.parse(document.getElementById('user_id').textContent);
        $(".infinite-container-chat").scrollTop($(".infinite-container-chat")[0].scrollHeight);

        //let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        let ws_scheme = 'ws';
        const chatSocket = new WebSocket(
            ws_scheme 
            + '://'
            + window.location.host
            + '/ws/'
            + chat_id
        );
        
        window.onbeforeunload = function() {
            chatSocket.onclose = function () {}; // disable onclose handler first
            chatSocket.close();
        };

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            $('.infinite-container-chat').append('<div class="clear-both"></div>');
            let message = generate_chat_message(data, user_id);
            $('.infinite-container-chat').append(message.hide().fadeIn(500));
            $("#chat-content").scrollTop($("#chat-content")[0].scrollHeight);
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) { 
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message_uncleaned = messageInputDom.value;
            let message_cleaned = message_uncleaned.trim()
            
            if (message_cleaned != ""){
                chatSocket.send(JSON.stringify({
                    'message': message_cleaned,
                    'user_id': user_id,
                    'url' : window.location.pathname,
                }));
                messageInputDom.value = '';
            } else {
                messageInputDom.value = '';
            }
        };
    }
})

$(function(){
    $("#friend_search_form").on("submit", function (e) {
        e.preventDefault();
        
        search = $("#search_param").val()
        $("#search_param").html("")
        $("#friend-list").prepend($(".friend-thumb[class*='" + search + "']").hide().fadeIn(500))
    })

    $(".friend-thumb").on('click', function(){
        url = this.getAttribute('data-href')
        window.location.href = url;
    })
})

$(function(){
    
    if($('.infinite-container-chat')[0]){
        setTimeout(() => {
            var infinite_waypoint = new Waypoint.InfinitePrepend({
                onBeforePageLoad: function () {
                    $('.spinner-border').show();
                },
                onAfterPageLoad: function () {
                    $('.spinner-border').hide();
                },
              })
        }, 1000);
    }
})

function generate_chat_message(data, user_id) {
    if (data.user_id === user_id){
        selector = "#user_hidden_message";
    } else {
        selector = "#friend_hidden_message";
    }
    let message = $(selector).clone().removeClass('hidden');
    message.find("#text").html(data.message);
    return message;
}
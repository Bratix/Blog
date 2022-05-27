$(function(){
    /* $('#search_friend_chat').on('change', function(e){
        let redirect = this.value 
        window.location.href = redirect;
    })

    $('.chat-select').on('click', function(e){
        let redirect = $(this).data("href") 
        console.log("redirect" + redirect)
        window.location.href = redirect;
    }) */
    
    let url = window.location.href
    if (url.includes('chat')){
        const chat_id = JSON.parse(document.getElementById('chat_id').textContent);
        const user_id = JSON.parse(document.getElementById('user_id').textContent);
        $("#chat-content").fadeIn(500).scrollTop($("#chat-content")[0].scrollHeight);

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/'
            + chat_id
        );
        

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            $('.chat-content').append('<div class="clear-both"></div>');
            let message = generate_chat_message(data, user_id);
            $('.chat-content').append(message.hide().fadeIn(500));
            $("#chat-content").scrollTop($("#chat-content")[0].scrollHeight);
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message,
                'user_id': user_id
            }));
            messageInputDom.value = '';
        };
    }
})

function generate_chat_message(data, user_id) {
    if (data.user_id === user_id){
        selector = "#user_hidden_message"
    } else {
        selector = "#friend_hidden_message"
    }
    let message = $(selector).clone().removeClass('hidden');
    message.find("#text").html(data.message)
    return message
}
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
        $(".infinite-container-chat").fadeIn(500).scrollTop($(".infinite-container-chat")[0].scrollHeight);

        const chatSocket = new WebSocket(
            'ws://'
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
            if (e.keyCode === 13) {  // enter, return
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
                    'user_id': user_id
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
        console.log("there brah", $(".friend-thumb[class*='" + search + "']"))
        $("#friend-list").prepend($(".friend-thumb[class*='" + search + "']").hide().fadeIn(500))
    })

    $(".friend-thumb").on('click', function(){
        console.log(this)
        url = this.getAttribute('data-href')
        console.log(url)
        window.location.href = url;
    })
})

$(function(){
    
    if($('.infinite-container-chat')[0]){
        /* setTimeout(() => {
            var waypoint = new Waypoint({
                element: $("#trigger-load")[0],
                container: $("#after-this")[0],
                handler: function() {
                  console.log('triggered')
                },
                context: $("#chat-content")[0]
              })
            console.log(waypoint)
        }, 1000); */

        setTimeout(() => {
            var infinite_waypoint = new Waypoint.InfinitePrepend({
                onBeforePageLoad: function () {
                    $('.spinner-border').show();
                },
                onAfterPageLoad: function () {
                    $('.spinner-border').hide();
                },
              })
            console.log(infinite_waypoint.waypoint)
        }, 1000);
    }

    /* context: $("#chat-content")[0],
    element: $("#trigger-load")[0],
    container: $("#after-this")[0], 
    
    offset: 0,
    items: '.infinite-item',
    more: '.infinite-more-link',
    loadingClass: 'infinite-loading',
    onBeforePageLoad: $.noop,
    onAfterPageLoad: $.noop */
    /* if($('.infinite-container-chat')[0]){
        setTimeout(() => {
            WaypointConf = {
                context: $("#chat-content")[0],
                element: $("#trigger-load")[0],
                container: $("#after-this")[0], 
                items: '.infinite-item',
                more: '.infinite-more-link',
                loadingClass: 'infinite-loading',
                onBeforePageLoad: $.noop,
                onAfterPageLoad: $.noop
            }

            
            

            var waypoint = new Waypoint({
                element: $("#trigger-load")[0],
                container: $("#after-this")[0],
                onBeforePageLoad: function () {
                    $('.spinner-border').show();
                },
                onAfterPageLoad: function () {
                    $('.spinner-border').hide();
                },
                handler: function() {
                  console.log('waypoint hit')
                    $.proxy(function() {
                      onBeforePageLoad()
                      waypoint.destroy()
                      $("#after-this").addClass(this.options.loadingClass)
                      
                      $.get($('.infinite-more-link').attr('href'), $.proxy(function(data) {
                        var $data = $($.parseHTML(data))
                        var $newMore = $data.find('.infinite-more-link')
                
                        var $items = $data.find('.infinite-item')
                        if (!$items.length) {
                          $items = $data.filter('.infinite-item')
                        }
                
                        $("#after-this").after($items)
                        $("#after-this").removeClass(this.options.loadingClass)
                
                        if (!$newMore.length) {
                          $newMore = $data.filter('.infinite-more-link')
                        }
                        if ($newMore.length) {
                          $('.infinite-more-link').replaceWith($newMore)
                          $more = $newMore
                          waypoint = new Waypoint(this.options)
                        }
                        else {
                          this.$more.remove()
                        }
                
                        this.options.onAfterPageLoad($items)
                      }, this))
                    }, this)
                  
                },
                context: $("#chat-content")[0]
              })
        }, 1000);
    } */
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
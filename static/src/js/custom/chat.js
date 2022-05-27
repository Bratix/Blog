$(function(){
    $('#search_friend_chat').on('change', function(e){
        let redirect = this.value 
        window.location.href = redirect;
    })

    $('.chat-select').on('click', function(e){
        let redirect = $(this).data("href") 
        console.log("redirect" + redirect)
        window.location.href = redirect;
    })
})
$(document).ready(function(){

        var text = $(".textarea-update").data("value")
        console.log("text", text)
        $(".textarea-update").html(text)

        var tags = $(".tag-class").text().replace(/ /g,'');
        console.log("text",tags)
        $(".taggit-input").val(tags)
        
})
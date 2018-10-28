$(document).ready(function(){

        var text = $(".textarea-update").data("value")
        $(".textarea-update").html(text)

        var tags = $(".tag-class").text().replace(/ /g,'');
        $(".taggit-input").val(tags)
        
})
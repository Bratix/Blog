$(document).ready(function(){
    var cat = $(".category_preselected").data("value")
    console.log("kategorija",$.trim(cat))
    $(".category_preselected").val(cat);
})
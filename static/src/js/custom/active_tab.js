$(document).ready(function(){
    let activeTab = $("#active_tab").text()
    if ($(("#" + activeTab)).hasClass("side-menu-main")) {
        $(("#" + activeTab)).addClass("side-menu--active")
    } else {
        $(("#" + activeTab)).addClass("side-menu--active")
        $(("#" + activeTab)).parent().parent().addClass('side-menu__sub-open').parent().find(".side-menu-main").addClass("side-menu--active")
    }
})
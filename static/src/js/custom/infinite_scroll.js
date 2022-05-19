import 'waypoints/lib/jquery.waypoints.min.js';
import 'waypoints/lib/shortcuts/infinite.min.js';


$(function(){
    setTimeout(() => {
        var infinite = new Waypoint.Infinite({
            element: $('.infinite-container')[0],
            onBeforePageLoad: function () {
            $('.spinner-border').show();
                setTimeout(() => {
                    $('.spinner-border').hide();
                }, 2000)
            },
    
            onAfterPageLoad: function () {
            $('.spinner-border').hide();
            }
    
        })
        Waypoint.refreshAll();
        
    }, 500)
})

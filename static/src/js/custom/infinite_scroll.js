import 'waypoints/lib/jquery.waypoints.min.js';
import 'waypoints/lib/shortcuts/infinite.min.js';


$(function(){
    var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
        $('.spinner-border').show();
        },

        onAfterPageLoad: function () {
        $('.spinner-border').hide();
        },

    })
})

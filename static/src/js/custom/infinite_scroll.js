import 'waypoints/lib/jquery.waypoints.min.js';
import 'waypoints/lib/shortcuts/infinite.min.js';

if ( $( ".infinite-container" ).length ) {
    let infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        handler: function(direction) {},
        offset: 'bottom-in-view',
        
        onBeforePageLoad: function () {
        $('.spinner-border').show();
        },
        onAfterPageLoad: function () {
        $('.spinner-border').hide();
        }
    })

}
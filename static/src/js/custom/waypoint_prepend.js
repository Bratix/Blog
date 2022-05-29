(function() {
    
    var $ = window.jQuery
    var Waypoint = window.Waypoint

    /* http://imakewebthings.com/waypoints/shortcuts/infinite-scroll */
    function InfinitePrepend(options) {
      this.options = $.extend({}, InfinitePrepend.defaults, options)
      this.container = this.options.element
      
      if (this.options.container !== 'auto') {
        this.container = this.options.container
      }
      
      this.$container = $(this.container)
      this.$more = $(this.options.more)
      if (this.$more.length) {
        this.setupHandler()
        this.waypoint = new Waypoint(this.options)
      }
    }
  
    /* Private */
    InfinitePrepend.prototype.setupHandler = function() {
      this.options.handler = $.proxy(function() {
        this.options.onBeforePageLoad()
        this.destroy()
        this.$container.addClass(this.options.loadingClass)
        
        $.get($(this.options.more).attr('href'), $.proxy(function(data) {
          var $data = $($.parseHTML(data))
          var $newMore = $data.find(this.options.more)
  
          var $items = $data.find(this.options.items)
          if (!$items.length) {
            $items = $data.filter(this.options.items)
          }
  
          this.$container.after($items)
          this.$container.removeClass(this.options.loadingClass)
  
          if (!$newMore.length) {
            $newMore = $data.filter(this.options.more)
          }
          if ($newMore.length) {
            this.$more.replaceWith($newMore)
            this.$more = $newMore
            this.waypoint = new Waypoint(this.options)
          }
          else {
            this.$more.remove()
          }
  
          this.options.onAfterPageLoad($items)
        }, this))
      }, this)
    }
  
    /* Public */
    InfinitePrepend.prototype.destroy = function() {
      if (this.waypoint) {
        this.waypoint.destroy()
      }
    }
  
    InfinitePrepend.defaults = {
      context: $("#chat-content")[0],
      element: $("#trigger-load")[0],
      container: $("#trigger-load")[0], 
      
      offset: 0,
      items: '.infinite-item',
      more: '.infinite-more-link',
      loadingClass: 'infinite-loading',
      onBeforePageLoad: $.noop,
      onAfterPageLoad: $.noop
    }
  
    Waypoint.InfinitePrepend = InfinitePrepend
  }())
  ;
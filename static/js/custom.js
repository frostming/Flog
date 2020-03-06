(function($) {
  var toggle = document.getElementById('menu-toggle')
  var menu = document.getElementById('menu')
  var close = document.getElementById('menu-close')

  toggle.addEventListener('click', function(e) {
    if (menu.classList.contains('open')) {
      menu.classList.remove('open')
    } else {
      menu.classList.add('open')
    }
  })

  close.addEventListener('click', function(e) {
    menu.classList.remove('open')
  })

  // Close menu after click on smaller screens
  $(window).on('resize', function() {
    if ($(window).width() < 846) {
      $('.main-menu a').on('click', function() {
        menu.classList.remove('open')
      })
    }
  })

  $('.owl-carousel').owlCarousel({
    items: 4,
    lazyLoad: true,
    loop: true,
    dots: true,
    margin: 30,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1
      },
      600: {
        items: 1
      },
      1000: {
        items: 1
      }
    }
  })

  $('.hover').mouseleave(function() {
    $(this).removeClass('hover')
  })

  $('.isotope-wrapper').each(function() {
    var $isotope = $('.isotope-box', this)
    var $filterCheckboxes = $('input[type="radio"]', this)

    var filter = function() {
      var type = $filterCheckboxes.filter(':checked').data('type') || '*'
      if (type !== '*') {
        type = '[data-type="' + type + '"]'
      }
      $isotope.isotope({ filter: type })
    }

    $isotope.isotope({
      itemSelector: '.isotope-item',
      layoutMode: 'masonry'
    })

    $(this).on('change', filter)
    filter()
  })

  lightbox.option({
    resizeDuration: 200,
    wrapAround: true
  })

  var $pswp = $('.pswp')
  if ($pswp.length === 0) return
  $pswp = $pswp[0]

  var getItems = function() {
    var items = []
    $('figure img').each(function() {
      var src = $(this).attr('src')
      var width = this.naturalWidth
      var height = this.naturalHeight

      var item = {
        src: src,
        w: width,
        h: height,
        el: this
      }
      var figcaption = $(this)
        .find('+figcaption')
        .first()
      if (figcaption.length !== 0) item.title = figcaption.html()
      items.push(item)
    })
    return items
  }

  var bindEvent = function() {
    var items = getItems()
    $('figure img').each(function(i) {
      $(this).on('click', function(e) {
        e.preventDefault()

        var options = {
          index: i,
          getThumbBoundsFn: function(index) {
            // See Options->getThumbBoundsFn section of docs for more info
            var thumbnail = items[index].el
            var pageYScroll =
              window.pageYOffset || document.documentElement.scrollTop
            var rect = thumbnail.getBoundingClientRect()

            return {
              x: rect.left,
              y: rect.top + pageYScroll,
              w: rect.width
            }
          }
        }

        // Initialize PhotoSwipe
        var gallery = new PhotoSwipe(
          $pswp,
          PhotoSwipeUI_Default,
          items,
          options
        )
        gallery.listen('gettingData', function(index, item) {
          if (item.w < 1 || item.h < 1) {
            // unknown size
            var img = new Image()
            img.onload = function() {
              // will get size after load
              item.w = this.width // set image width
              item.h = this.height // set image height
              gallery.invalidateCurrItems() // reinit Items
              gallery.updateSize(true) // reinit Items
            }
            img.src = item.src // let's download image
          }
        })
        gallery.init()
      })
    })
  }
  bindEvent()
})(jQuery)

function hasTouchScreen() {
  let result = false
  if ('maxTouchPoints' in navigator) {
    result = navigator.maxTouchPoints > 0
  } else if ('msMaxTouchPoints' in navigator) {
    result = navigator.msMaxTouchPoints > 0
  } else {
    var mQ = window.matchMedia && matchMedia('(pointer:coarse)')
    if (mQ && mQ.media === '(pointer:coarse)') {
      result = !!mQ.matches
    } else if ('orientation' in window) {
      result = true // deprecated, but good fallback
    } else {
      // Only as a last resort, fall back to user agent sniffing
      var UA = navigator.userAgent
      result = (
        /\b(BlackBerry|webOS|iPhone|IEMobile)\b/i.test(UA) ||
        /\b(Android|Windows Phone|iPad|iPod)\b/i.test(UA)
      )
    }
  }
  return result
}

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
  });

  (function() {
    var $pswp = $('.pswp')
    if ($pswp.length === 0) return
    $pswp = $pswp[0]

    var getItems = function() {
      var items = []
      $('.article-body figure img').each(function() {
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
      $('.article-body figure img').each(function(i) {
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
  })()

  function search(text) {
    fetch(window.searchApiUrl + `?q=${text}`).then(resp => resp.json()).then(data => {
      $('#search-modal .modal-body').html('')
      data.data.items.forEach(post => {
        const title = post.title.replace(new RegExp(`(${text})`, 'ig'), '<span class="search-hll">$1</span>')
        const content = post.content.replace(new RegExp(`(${text})`, 'ig'), '<span class="search-hll">$1</span>')
        $(`<div class="search-result-item"><h6><a href="${post.url}">${title}</a></h6><p>${content}</p></div>`).appendTo($('#search-modal .modal-body'))
      })
    })
  }
  $(function() {
    $('input#search-text').bind('keydown', function(event) {
      if (event.keyCode === 13) {
        search(event.target.value)
        event.preventDefault()
      }
    })
    $('#search-modal button').click(function() {
      search($('input#search-text').val())
      return false
    })
  })
})(jQuery)

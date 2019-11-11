var hasMobileUA = function() {
  var nav = window.navigator;
  var ua = nav.userAgent;
  var pa = /iPad|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP|IEMobile|Symbian/g;

  return pa.test(ua);
};
var isMobile = function() {
  return window.screen.width < 767 && this.hasMobileUA();
};
$(document).ready(function() {
  var headerHeight = $(".page-head").outerHeight();
  $(window).on("scroll", function() {
    var $navbar = $("nav.navbar");
    $navbar.toggleClass("navbar-light", window.pageYOffset >= headerHeight);
    $navbar.toggleClass("navbar-dark", window.pageYOffset < headerHeight);
    $("#totop").toggleClass(
      "invisible",
      $(window).scrollTop() < $(window).height() * 0.8
    );
    $("#totop").toggleClass(
      "visible",
      $(window).scrollTop() > $(window).height() * 0.8
    );
  });

  $(window).on(
    "scroll",
    {
      previousTop: 0
    },
    function() {
      $("nav.navbar").toggleClass(
        "hide",
        $(window).scrollTop() > this.previousTop
      );
      this.previousTop = $(window).scrollTop();
    }
  );

  $("body").scrollspy({
    target: ".post-toc",
    offset: 200
  });

  $("#totop").on("click", function() {
    $("html, body").animate(
      {
        scrollTop: 0
      },
      1000,
      function() {
        $("#totop")
          .removeClass("visible")
          .addClass("invisible");
      }
    );
  });

  $(".copy-code").on("click", function() {
    var code = $(this)
      .parent()
      .next("pre")
      .text();
    var el = document.createElement("textarea");
    el.value = code; // Set its value to the string that you want copied
    el.setAttribute("readonly", ""); // Make it readonly to be tamper-proof
    el.style.position = "absolute";
    el.style.left = "-9999px"; // Move outside the screen to make it invisible
    document.body.appendChild(el); // Append the <textarea> element to the HTML document
    const selected =
      document.getSelection().rangeCount > 0 // Check if there is any content selected previously
        ? document.getSelection().getRangeAt(0) // Store selection if found
        : false; // Mark as false to know no selection existed before
    el.select(); // Select the <textarea> content
    document.execCommand("copy"); // Copy - only works as a result of a user action (e.g. click events)
    document.body.removeChild(el); // Remove the <textarea> element
    if (selected) {
      // If a selection existed before copying
      document.getSelection().removeAllRanges(); // Unselect everything on the HTML document
      document.getSelection().addRange(selected); // Restore the original selection
    }
    return false;
  });
});

$(function() {
  var $pswp = $(".pswp");
  if ($pswp.length === 0) return;
  $pswp = $pswp[0];
  var currentLoad = 0;

  var getItems = function() {
    var items = [];
    $("figure img").each(function() {
      var src = $(this).attr("src");
      var width = this.naturalWidth;
      var height = this.naturalHeight;

      var item = {
        src: src,
        w: width,
        h: height,
        el: this
      };
      var figcaption = $(this)
        .find("+figcaption")
        .first();
      if (figcaption.length !== 0) item.title = figcaption.html();
      items.push(item);
    });
    return items;
  };

  var bindEvent = function() {
    var items = getItems();
    $("figure img").each(function(i) {
      $(this).on("click", function(e) {
        e.preventDefault();

        var options = {
          index: i,
          getThumbBoundsFn: function(index) {
            // See Options->getThumbBoundsFn section of docs for more info
            var thumbnail = items[index].el;
            var pageYScroll =
              window.pageYOffset || document.documentElement.scrollTop;
            var rect = thumbnail.getBoundingClientRect();

            return {
              x: rect.left,
              y: rect.top + pageYScroll,
              w: rect.width
            };
          }
        };

        // Initialize PhotoSwipe
        var gallery = new PhotoSwipe(
          $pswp,
          PhotoSwipeUI_Default,
          items,
          options
        );
        gallery.listen("gettingData", function(index, item) {
          if (item.w < 1 || item.h < 1) {
            // unknown size
            var img = new Image();
            img.onload = function() {
              // will get size after load
              item.w = this.width; // set image width
              item.h = this.height; // set image height
              gallery.invalidateCurrItems(); // reinit Items
              gallery.updateSize(true); // reinit Items
            };
            img.src = item.src; // let's download image
          }
        });
        gallery.init();
      });
    });
  };
  bindEvent();
});

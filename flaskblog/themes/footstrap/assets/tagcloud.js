(function($) {

  $.fn.tagcloud = function(options) {
    var opts = $.extend({}, $.fn.tagcloud.defaults, options);
    tagWeights = this.map(function(){
      return $(this).attr("rel");
    });
    tagWeights = jQuery.makeArray(tagWeights).sort(compareWeights);
    lowest = tagWeights[0];
    highest = tagWeights.pop();
    range = highest - lowest;
    if(range === 0) {range = 1;}
    // Sizes
    if (opts.size) {
      fontIncr = (opts.size.end - opts.size.start)/range;
    }
    // Colors
    if (opts.color) {
      colorIncr = colorIncrement (opts.color, range);
    }
    return this.each(function() {
      weighting = $(this).attr("rel") - lowest;
      if (opts.size) {
        $(this).css({"font-size": opts.size.start + (weighting * fontIncr) + opts.size.unit});
      }
      if (opts.color) {
        // change color to background-color
        $(this).css({"background-color": tagColor(opts.color, colorIncr, weighting)});
      }
    });
  };

  $.fn.tagcloud.defaults = {
    size: {start: 14, end: 18, unit: "pt"}
  };

  // Converts hex to an RGB array
  function toRGB (code) {
    if (code.length == 4) {
      code = jQuery.map(/\w+/.exec(code), function(el) {return el + el; }).join("");
    }
    hex = /(\w{2})(\w{2})(\w{2})/.exec(code);
    return [parseInt(hex[1], 16), parseInt(hex[2], 16), parseInt(hex[3], 16)];
  }

  // Converts an RGB array to hex
  function toHex (ary) {
    return "#" + jQuery.map(ary, function(i) {
      hex =  i.toString(16);
      hex = (hex.length == 1) ? "0" + hex : hex;
      return hex;
    }).join("");
  }

  function colorIncrement (color, range) {
    return jQuery.map(toRGB(color.end), function(n, i) {
      return (n - toRGB(color.start)[i])/range;
    });
  }

  function tagColor (color, increment, weighting) {
    rgb = jQuery.map(toRGB(color.start), function(n, i) {
      ref = Math.round(n + (increment[i] * weighting));
      if (ref > 255) {
        ref = 255;
      } else {
        if (ref < 0) {
          ref = 0;
        }
      }
      return ref;
    });
    return toHex(rgb);
  }

  function compareWeights(a, b)
  {
    return a - b;
  }

})(jQuery);


$(window).load(function(){

	/* For quick copy-paste */
    $('input').focus(function(){this.select();});

	/* Change color on every key input. */
	$('#hex').bind('blur keydown', function (event) {
		var el = this;
		setTimeout(function () {
			var rgb = [],
			    $input = $(el),
			    fail = false,
			    original = $input.val(),

			hex = (original+'').replace(/#/, '');

			if (original.length === 1 && original !== '#') { $input.val('#' + original); }
			if (hex.length == 3) hex = hex + hex;

			for (var i = 0; i < 6; i+=2) {
			   rgb.push(parseInt(hex.substr(i,2),16));
			   fail = fail || rgb[rgb.length - 1].toString() === 'NaN';
			}

			$('#rgb').val(fail ? '' : 'rgb(' + rgb.join(',') + ')');
			$('#hsl').val(fail ? '' : 'hsl(' + rgbToHsl.apply(null, rgb).join(',') + ')');

			$('body').css('backgroundColor', $('#rgb').val());
	    }, 13);
	});

    /* Function to convert rgb-to-hsl. */

	function rgbToHsl(r, g, b){
		r /= 255, g /= 255, b /= 255;
		var max = Math.max(r, g, b), min = Math.min(r, g, b);
		var h, s, l = (max + min) / 2;

		if (max == min) { h = s = 0; }
		else {
			var d = max - min;
			s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

			switch (max){
				case r: h = (g - b) / d + (g < b ? 6 : 0); break;
				case g: h = (b - r) / d + 2; break;
				case b: h = (r - g) / d + 4; break;
			}

			h /= 6;
		}

		return [(h*100+0.5)|0, ((s*100+0.5)|0) + '%', ((l*100+0.5)|0) + '%'];
	}
});


$(document).ready(function() {

    if ( !("placeholder" in document.createElement("input")) ) {
        $("input[placeholder], textarea[placeholder]").each(function() {
            var val = $(this).attr("placeholder");
            if ( this.value == "" ) {
                this.value = val;
            }
            $(this).focus(function() {
                if ( this.value == val ) {
                    this.value = "";
                }
            }).blur(function() {
                if ( $.trim(this.value) == "" ) {
                    this.value = val;
                }
            })
        });

        // Clear default placeholder values on form submit
        $('form').submit(function() {
            $(this).find("input[placeholder], textarea[placeholder]").each(function() {
                if ( this.value == $(this).attr("placeholder") ) {
                    this.value = "";
                }
            });
        });
    }
});

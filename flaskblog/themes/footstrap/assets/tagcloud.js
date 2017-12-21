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
        var color = tagColor(opts.color, colorIncr, weighting);
        $(this).css({"border-color": color, "color": color});
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
    return jQuery.map(rgbToHsl(toRGB(color.end)), function(n, i) {
      return (n - rgbToHsl(toRGB(color.start))[i])/range;
    });
  }

  function tagColor (color, increment, weighting) {
    hsl = jQuery.map(rgbToHsl(toRGB(color.start)), function(n, i) {
      ref = n + (increment[i] * weighting);
      if (ref > 1) {
        ref = 1;
      } else {
        if (ref < 0) {
          ref = 0;
        }
      }
      return ref;
    });
    return toHex(hslToRgb(hsl));
  }

  function compareWeights(a, b)
  {
    return a - b;
  }

  function rgbToHsl(array){
  	var r = array[0]/255, g = array[1]/255, b = array[2]/255;
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

  	return [h, s, l];
  }

  function hslToRgb(array) {
    var h = array[0], s = array[1], l = array[2];
    var r, g, b;

    if(s == 0){
        r = g = b = l; // achromatic
    }else{
      var hue2rgb = function hue2rgb(p, q, t){
          if(t < 0) t += 1;
          if(t > 1) t -= 1;
          if(t < 1/6) return p + (q - p) * 6 * t;
          if(t < 1/2) return q;
          if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
          return p;
      }

      var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      var p = 2 * l - q;
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
  }

  return [(r*255+0.5)|0, (g*255+0.5)|0, (b*255+0.5)|0];
  }
})(jQuery);

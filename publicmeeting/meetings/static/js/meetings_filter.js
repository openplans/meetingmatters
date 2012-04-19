function initTopicFilter(tag) {
  var $li = $('#id_tags-' + tag + '-li'),
      $btn = $('#id_tags-' + tag + '-btn'),
      $chk = $('#id_tags-' + tag);

  if ($li.length !== 1)
    console.error('The check box must be inside of a list item.');

  if ($btn.length !== 1)
    console.error('The check box should have a link to go with it.');

  $btn.click(function() {
    if ($chk.is(':checked')) {
      $chk.removeAttr('checked');
    } else {
      $chk.attr('checked', 'checked');
    }
    $chk.trigger('change');
  });

  $chk.change(function() {
    if ($chk.is(':checked')) {
      $li.addClass('active');
    } else {
      $li.removeClass('active');
    }
  });
}


function initAllTopicsFilter() {
  var $li = $('#id_all_tags-li'),
      $btn = $('#id_all_tags-btn'),
      $chk = $('input[name="tags"]'),
      $form = $('#id_filter_form');

  $btn.click(function() {
    $chk.removeAttr('checked');
    $chk.trigger('change');
  });

  $chk.change(function() {
    if ($chk.filter(':checked').length > 0) {
      $li.removeClass('active');
    } else {
      $li.addClass('active');
    }
  });
}

/**
 * The widget that goes with these methods is in floppyforms/meetings_bbmap.html
 */
function initGeoBoundsMap(map, value, fieldid, provider) {
  var n, e, s, w,

      // Which map provider are we using, Google or Leaflet
      isG = (google && google.maps && provider === google.maps),
      isL = !isG;

  if (value) {
    var splitVal = value.split(',');
    n = parseFloat(splitVal[0]);
    e = parseFloat(splitVal[1]);
    s = parseFloat(splitVal[2]);
    w = parseFloat(splitVal[3]);
  } else {
    n = 75;
    e = 0;
    s = -75;
    w = 359.999;
  }

  if (isL) {
    var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png',
        cloudmadeAttribution = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
        cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttribution}),
        mapBounds;

    mapBounds = new L.LatLngBounds(new L.LatLng(n, e), new L.LatLng(s, w));
    map.fitBounds(mapBounds);
    map.addLayer(cloudmade);
    map.on('moveend', function(evt) {
      setGeoFilterValues(map, fieldid, L);
    });
  } else if (isG) {
    var G = provider,
        mapBounds;

    mapBounds = new G.LatLngBounds(new G.LatLng(s, w), new G.LatLng(n, e));
    map.fitBounds(mapBounds);
    google.maps.event.addListener(map, 'bounds_changed', function() {
      setGeoFilterValues(map, fieldid, G);
    });
  }
}

function toggleGeoBoundsMap(map, fieldid, provider) {
  var geofilter = $('#' + fieldid + '-enable').is(':checked');
  if (geofilter) {
    $('#' + fieldid + '-map-container').css({position: 'static'});
  } else {
    // If we hide the map, it won't load it's tiles (if we're using Google), so
    // let's just move it far off the page.
    $('#' + fieldid + '-map-container').css({position:'absolute', left: -10000});
  }

  // As soon as the map has bounds, update the filter value.
  var _setGeoFilterValues = function(map, fieldid, provider) {
    if (map.getBounds()) {
      setGeoFilterValues(map, fieldid, provider);
    } else {
      setTimeout(function() {
        _setGeoFilterValues(map, fieldid, provider)
      }, 100);
    }
  };
  _setGeoFilterValues(map, fieldid, provider);
}

function setGeoFilterValues(map, fieldid, provider) {
  var geofilter = $('#' + fieldid + '-enable').is(':checked'),

      // Which map provider are we using, Google or Leaflet
      isG = (google && google.maps && provider === google.maps),
      isL = !isG;

  if (geofilter) {
    var mb = map.getBounds(),
        n, e, s, w;

    if (isL) {
      n = mb._northEast.lat;
      e = mb._northEast.lng;
      s = mb._southWest.lat;
      w = mb._southWest.lng;
    } else if (isG) {
      n = mb.getNorthEast().lat();
      e = mb.getNorthEast().lng();
      s = mb.getSouthWest().lat();
      w = mb.getSouthWest().lng();
    }

    bbox = n + ',' + e + ',' + s + ',' + w;
    $('#' + fieldid).val(bbox);
  } else {
    $('#' + fieldid).removeAttr('value');
  }
}

function togglePlaceFilterVisibility() {
  if ($('#id_place-filter-wrapper').css('position') == 'static')
    hidePlaceFilter();
  else
    $('#id_place-filter-wrapper').css({position: 'static'});
}

function toggleTimeFilterVisibility() {
  $('#id_time-filter-wrapper').slideToggle();
}

function toggleTopicsFilterVisibility() {
  $('#id_topics-filter-wrapper').slideToggle();
}

function hidePlaceFilter() {
  $('#id_place-filter-wrapper').css({position:'absolute', left: -10000});
}

function hideTimeFilter() {
  $('#id_time-filter-wrapper').hide();
}

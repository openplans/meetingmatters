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
function initGeoBoundsMap(map, value) {
  var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png',
      cloudmadeAttribution = 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
      cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttribution}),
      mapBounds,
      n, e, s, w;

  if (value) {
    var splitVal = value.split(',');
    n = parseFloat(splitVal[0]);
    e = parseFloat(splitVal[1]);
    s = parseFloat(splitVal[2]);
    w = parseFloat(splitVal[3]);
  } else {
    n = 40.149488;
    e = -74.942551;
    s = 39.871804;
    w = -75.301666;
  }

  mapBounds = new L.LatLngBounds(new L.LatLng(n, e), new L.LatLng(s, w));
  map.fitBounds(mapBounds);
  map.addLayer(cloudmade);
  map.on('moveend', function(evt) {
    setGeoFilterValues(map);
  });
}

function toggleGeoBoundsMap(map, fieldid) {
  var geofilter = $('#' + fieldid + '-enable').is(':checked');
  if (geofilter) {
    $('#' + fieldid + '-map-wrapper').show();
  } else {
    $('#' + fieldid + '-map-wrapper').hide();
  }
}

function setGeoFilterValues(map, fieldid) {
  var geofilter = $('#' + fieldid + '-enable').is(':checked');
  if (geofilter) {
    var mb = map.getBounds(),
        ne = mb._northEast,
        sw = mb._southWest;
    bbox = ne.lat + ',' + ne.lng + ',' + sw.lat + ',' + sw.lng;
    $('#' + fieldid).val(bbox);
  } else {
    $('#' + fieldid).removeAttr('value');
  }
}

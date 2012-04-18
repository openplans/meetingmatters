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

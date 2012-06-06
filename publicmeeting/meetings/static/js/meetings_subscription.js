function initRssLinkPopover() {
  var $link = $('#id_rss-link');

  $link.popover({
    placement: 'bottom',
    content: '<p>Right-click the link, copy it, and add it to your RSS reader</p>',
    delay: { show: 0, hide: 300 }
  });
}

function initIcsLinkPopover() {
  var $link = $('#id_ical-link');

  $link.popover({
    placement: 'bottom',
    content: '<p>Right-click the link, copy it, and add it to your calendar</p><p>For more information: <a href="http://support.google.com/calendar/bin/answer.py?hl=en&answer=37100" target="_blank">Google</a>, <a href="http://www.apple.com/findouthow/mac/#subscribeical" target="_blank">iCalendar</a>, <a href="http://office.microsoft.com/en-us/outlook-help/view-and-subscribe-to-internet-calendars-HA010167325.aspx#BM2" target="_blank">Outlook</a></p>',
    delay: { show: 0, hide: 2000 }
  });
}

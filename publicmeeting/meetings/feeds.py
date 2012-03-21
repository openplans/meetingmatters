from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django_cal.views import Events
from taggit.models import Tag

from . import models

class MeetingListFeedMixin (object):
    tag_slugs = []
    querystring = None

    def title(self):
        title = u'Public meetings'
        if self.tag_slugs:
            title += u' tagged with "'
            title += u'", "'.join([tag.name for tag in self.tags()])
            title += u'"'
        return title

    def description(self):
        description = self.title() + u' from http://meetingmatters.org/'
        return description

    def link(self):
        link = reverse('browse_meetings_meeting_list')
        if self.querystring:
            link += u'?' + self.querystring
        return link

    def tags(self):
        return Tag.objects.filter(slug__in=self.tag_slugs)

    def get_object(self, request, *args, **kwargs):
        self.tag_slugs = request.GET.getlist('tags')
        self.querystring = request.GET.urlencode()

    def items(self):
        # For RSS, how should these be ordered?
        queryset = models.Meeting.objects.all().order_by('created_datetime')
        tag_slugs = self.tag_slugs

        if tag_slugs:
            queryset = queryset.filter(tags__slug__in=tag_slugs).distinct()

        return queryset

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description


class MeetingListRss (MeetingListFeedMixin, Feed):
    pass


class MeetingListICal (MeetingListFeedMixin, Events):
    def item_start(self, item):
        return item.begin_time

    def item_end(self, item):
        return item.end_time

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from . import models

class MeetingListFeed (Feed):
    def link(self):
        return reverse('browse_meetings_meeting_list')

    def get_object(self, request, *args, **kwargs):
        self.tag_slugs = request.GET.getlist('tags')

    def items(self):
        # For RSS, you supposedly want to see when people create new meetings
        # in your stream.
        queryset = models.Meeting.objects.all().order_by('created_datetime')
        tag_slugs = self.tag_slugs

        if tag_slugs:
            queryset = queryset.filter(tags__slug__in=tag_slugs).distinct()

        return queryset

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

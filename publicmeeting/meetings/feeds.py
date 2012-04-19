from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django_cal.views import Events
from taggit.models import Tag

from . import forms
from . import models
from .views import browse as views

class MeetingListFeedMixin (views.MeetingListMixin):
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
        current_site = Site.objects.get_current()
        description = self.title() + u' from ' + current_site.domain
        return description

    def link(self):
        link = reverse('browse_meetings_meeting_list')
        if self.querystring:
            link += u'?' + self.querystring
        return link

    def tags(self):
        return Tag.objects.filter(slug__in=self.tag_slugs)

    def get_object(self, request, *args, **kwargs):
        self.form = forms.MeetingFilters(data=request.GET)
        self.tag_slugs = request.GET.getlist('tags')
        self.querystring = request.GET.urlencode()

    def items(self):
        # For RSS, how should these be ordered?
        if self.form.is_valid():
            queryset = self.get_meetings(**self.form.cleaned_data).order_by('created_datetime')
        else:
            queryset = models.Meeting.objects.none()

        return queryset

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_categories(self, item):
        return [tag.name for tag in item.tags.all()]


class MeetingListRss (MeetingListFeedMixin, Feed):
    pass


class MeetingListICal (MeetingListFeedMixin, Events):
    def item_start(self, item):
        return item.begin_time

    def item_end(self, item):
        return item.end_time

    def cal_name(self):
        return self.title()

    def cal_desc(self):
        return self.description()

    def item_summary(self, item):
        return self.item_title(item)

    def item_location(self, item):
        return item.venue_name

    def item_created(self, item):
        return item.created_datetime

    def item_last_modified(self, item):
        return item.updated_datetime

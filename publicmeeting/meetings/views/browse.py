from django.core.urlresolvers import reverse
from django.contrib.gis import geos
from django.http import HttpResponseRedirect
from django.views import generic as views
from taggit import models as taggit_models
import logging
import urllib

from .. import models
from .. import forms

class MeetingListMixin (object):
    def get_meetings(self, earliest=None, latest=None, tags=[], center=None, radius=None, bbox=None, canceled=False, **extra):
        """
        tags -- A list of tag slugs
        extra -- This should usually be empty

        """
        assert len(extra) == 0

        # Start with all the objects, following foreign keys.  Specify the venue
        # explicitly, since select_related doesn't follow potentially NULL
        # columns by default.
        meetings = models.Meeting.objects.all().select_related('venue')
        if not canceled:
            meetings = meetings.filter(canceled=False)
        if center and radius:
            meetings = meetings.filter(venue__location__distance_lte=(center, radius))
        if bbox:
            meetings = meetings.filter(venue__location__contained=bbox)
        if earliest:
            meetings = meetings.filter(end_time__gt=earliest)
        if latest:
            meetings = meetings.filter(begin_time__lt=latest)
        if tags:
            # This filter is a disjunction of the selected tags
            meetings = meetings.filter(tags__in=tags)

            # This filter is an adjunction of the selected tags
            #for tag in tags:
            #    meetings.filter(tags=tag)

        meetings = meetings.distinct().order_by('begin_time')
        return meetings.prefetch_related('minutes')

    def get_query_params(self):
        pass


class MeetingListView (MeetingListMixin, views.ListView):
    model = models.Meeting
    context_object_name = 'meetings'
    template_name = 'browse_meetings-meeting_list.html'

    def get_context_data(self, **kwargs):
        context = super(MeetingListView, self).get_context_data(**kwargs)

        tag_slugs = self.request.GET.getlist('tags')
        all_tags = models.MeetingTopic.ordered_objects.cached()
        selected_tags = models.MeetingTopic.objects.filter(slug__in=tag_slugs)

        context['tags'] = all_tags
        context['selected_tags'] = selected_tags

        context['rss_url'] = reverse('meeting_list_rss') + '?' + self.request.GET.urlencode()
        context['ical_url'] = reverse('meeting_list_ical') + '?' + self.request.GET.urlencode()

        context['filter_form'] = self.form

        return context

    def get_queryset(self):
        if self.form.is_valid():
            return self.get_meetings(**self.form.cleaned_data)
        else:
            logging.debug(self.form.errors)
            return []

    def get(self, request, *args, **kwargs):
        # If there are default filters in the session, and they are not
        # overridden with any query parameters, turn the filters into query
        # parameters and redirect to the current url using the parameters.
        default_filters = self.request.session.get('default_filters', {})
        if default_filters and not request.GET:
            query = urllib.urlencode(default_filters)
            return HttpResponseRedirect('?'.join([request.path, query]))

        # Otherwise, just use the normal get.
        self.form = forms.MeetingFilters(data=self.request.GET)
        return super(MeetingListView, self).get(request, *args, **kwargs)


class MeetingListPartialView (MeetingListView):
    template_name = 'partials/meetings_browse_meetings.html'


class MeetingDetailView (views.DetailView):
    model = models.Meeting
    context_object_name = 'meeting'
    template_name = 'browse_meetings-meeting_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        try:
            return models.Meeting.objects.select_related('venue').get(slug=slug)
        except models.Meeting.DoesNotExist:
            from django.http import Http404
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': models.Meeting._meta.verbose_name})

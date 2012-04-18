from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views
from taggit import models as taggit_models
import logging
import urllib

from .. import models
from .. import forms

class MeetingListMixin (object):
    def get_meetings(self, earliest=None, latest=None, tags=[], region=None, center=None, radius=None, **extra):
        """
        tags -- A list of tag slugs
        region -- A list of one region slug. If there are more than one, all
            but the last one are ignored.
        extra -- This should usually be empty

        """
        assert len(extra) == 0

        meetings = models.Meeting.objects.all().select_related()
        if region:
            meetings = meetings.filter(region=region)
        if center:
            meetings = meetings.filter(venue__location__distance_lte=(center, radius))
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
        return meetings

    def get_query_params(self):
        pass


class MeetingListView (MeetingListMixin, views.ListView):
    model = models.Meeting
    context_object_name = 'meetings'
    template_name = 'browse_meetings-meeting_list.html'

    def get_context_data(self, **kwargs):
        context = super(MeetingListView, self).get_context_data(**kwargs)

        tag_slugs = self.request.GET.getlist('tags')
        all_tags = taggit_models.Tag.objects.all().order_by('name')
        selected_tags = taggit_models.Tag.objects.filter(slug__in=tag_slugs)

        context['tags'] = [tag for tag in all_tags]
        context['selected_tags'] = selected_tags

        context['rss_url'] = reverse('meeting_list_rss') + '?' + self.request.GET.urlencode()
        context['ical_url'] = reverse('meeting_list_ical') + '?' + self.request.GET.urlencode()

        context['filter_form'] = self.form

        return context

    def get_queryset(self):
        if self.form.is_valid():
            return self.get_meetings(**self.form.cleaned_data)
        else:
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


class MeetingDetailView (views.DetailView):
    model = models.Meeting
    context_object_name = 'meeting'
    template_name = 'browse_meetings-meeting_detail.html'


class DefaultMeetingFilters (views.FormView):
    form_class = forms.DefaultFilters
    template_name = 'choose_region.html'

    def get_success_url(self):
        return reverse('project-home')

    def get_context_data(self, **kwargs):
        context = super(DefaultMeetingFilters, self).get_context_data(**kwargs)
        context['regions'] = models.Region.objects.all()
        return context

    def form_valid(self, form):
        default_filters = self.request.session.get('default_filters', {})

        region = form.cleaned_data.get('region', None)
        default_filters['region'] = region.slug if region else None

        self.request.session['default_filters'] = default_filters
        return super(DefaultMeetingFilters, self).form_valid(form)

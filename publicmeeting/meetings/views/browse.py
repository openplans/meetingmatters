from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views
from taggit import models as taggit_models
import logging
import urllib

from .. import models
from .. import forms

class MeetingListMixin (object):
    def get_meetings(self, tags=[], region=None, **extra):
        """
        tags -- A list of tag slugs
        region -- A list of one region slug. If there are more than one, all
            but the last one are ignored.
        extra -- This should usually be empty

        """
        assert len(extra) == 0

        # Start with all the meetings.
        meetings = models.Meeting.objects.all().select_related()

        # Filter by any tags.
        for tag in tags:
            meetings = meetings.filter(tags__slug=tag)

        # Filter by region.
        if region and isinstance(region, list):
            region = region[-1]

        if region:
            meetings = meetings.filter(region__slug=region)

        # Make sure each meeting is only in there once.
        meetings.distinct()

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

        context['tags'] = all_tags
        context['selected_tags'] = selected_tags

        context['rss_url'] = reverse('meeting_list_rss') + '?' + self.request.GET.urlencode()
        context['ical_url'] = reverse('meeting_list_ical') + '?' + self.request.GET.urlencode()

        for tag in all_tags:
            get_params = self.request.GET.copy()
            tag_slugs_copy = tag_slugs[:]
            if tag in selected_tags:
                tag_slugs_copy.remove(tag.slug)
            else:
                tag_slugs_copy.append(tag.slug)
            get_params.setlist('tags', tag_slugs_copy)
            tag.qs = get_params.urlencode()

        return context

    def get_queryset(self):
        filters = self.request.GET
        return self.get_meetings(**filters).order_by('-begin_time')

    def get(self, request, *args, **kwargs):
        # If there are default filters in the session, and they are not
        # overridden with any query parameters, turn the filters into query
        # parameters and redirect to the current url using the parameters.
        default_filters = self.request.session.get('default_filters', {})
        if default_filters and not request.GET:
            query = urllib.urlencode(default_filters)
            return HttpResponseRedirect('?'.join([request.path, query]))

        # Otherwise, just use the normal get.
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

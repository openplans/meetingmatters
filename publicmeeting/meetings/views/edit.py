from __future__ import division

import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import linebreaksbr, urlencode
from django.views import generic as views
from taggit import models as taggit_models
from uni_form.layout import Hidden

from utils.decorators import LoginRequired

from .. import forms
from .. import models

import logging
log = logging.getLogger(__name__)

@LoginRequired
class CheckForSimilarMeetingsView (views.FormView):
    form_class = forms.CheckForSimilarMeetingsForm
    template_name = 'create_meeting-search_similar.html'

    def get_success_url(self):
        return reverse('create_meeting_fill_info')

    def meeting_unique(self, form):
        self.save_workflow_data(form)
        return super(CheckForSimilarMeetingsView, self).form_valid(form)

    def meeting_duplicate(self, form, similar_meetings):
        # Allow the user to bypass the check on the second time
        form.helper.layout.fields[1].fields[0].value = "Continue Anyway"
        form.helper.layout.fields.append(Hidden('bypass_check', ''))

        return self.render_to_response(
            self.get_context_data(form=form,
                                  similar_meetings=similar_meetings))

    def form_valid(self, form):
        if 'bypass_check' in self.request.POST:
            return self.meeting_unique(form)

        meeting = models.Meeting(**form.cleaned_data)
        similar_meetings = meeting.similar_meetings()

        if similar_meetings:
            return self.meeting_duplicate(form, similar_meetings)
        else:
            return self.meeting_unique(form)

    def save_workflow_data(self, form):
        self.request.session['create_meeting-workflow'] = form.cleaned_data


class MeetingInfoFormViewMixin (object):
    def get_context_data(self, **kwargs):
        context = super(MeetingInfoFormViewMixin, self).get_context_data(**kwargs)

        venues_data = {}
        venues = models.Venue.objects.all()
        for venue in venues:
            venues_data[venue.pk] = {
                'name': venue.name,
                'address': venue.address,
                'encAddress': urlencode(venue.address),
                'lat': venue.location.y,
                'lng': venue.location.x
            }
        context['venues_json'] = json.dumps(venues_data)
        context['venue_form'] = forms.VenueForm()
        return context


@LoginRequired
class CreateMeetingInfoView (MeetingInfoFormViewMixin, views.CreateView):
    model = models.Meeting
    form_class = forms.FillInMeetingInfoForm
    template_name = 'edit_meeting-fill_info.html'

    def get_success_url(self):
        return reverse('browse_meetings_meeting_detail', kwargs={'slug': self.object.slug})

    def get_workflow_data(self):
        workflow_data = self.request.session.get('create_meeting-workflow')
        return workflow_data or {}

    def get_form_kwargs(self):
        self.object = models.Meeting(**self.get_workflow_data())

        default_filters = self.request.session.get('default_filters', {})
        if 'region' in default_filters:
            try:
                self.object.region = models.Region.objects.get(slug=default_filters['region'])
            except models.Region.DoesNotExist:
                pass

        return super(CreateMeetingInfoView, self).get_form_kwargs()

@LoginRequired
class UpdateMeetingInfoView (MeetingInfoFormViewMixin, views.UpdateView):
    model = models.Meeting
    form_class = forms.FillInMeetingInfoForm
    template_name = 'edit_meeting-fill_info.html'

    def get_success_url(self):
        return reverse('browse_meetings_meeting_detail', kwargs={'slug': self.object.slug})


@LoginRequired
class CreateVenueInfoView (views.CreateView):
    model = models.Venue
    form_class = forms.VenueForm
    template_name = 'partials/meeting_edit_venue.html'

    def form_valid(self, form):
        venue = self.object = form.save()
        venue_data = {
            'name': venue.name,
            'address': venue.address,
            'encAddress': urlencode(venue.address),
            'lat': venue.location.y,
            'lng': venue.location.x,
            'pk': venue.pk
        }

        return HttpResponse(json.dumps(venue_data), content_type="application/json", status=201)

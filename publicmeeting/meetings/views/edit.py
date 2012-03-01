from __future__ import division
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views
from taggit import models as taggit_models
from uni_form.layout import Hidden

from project.utils.decorators import LoginRequired

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

    def check_for_similar_meetings(self, form, threshold=0.5):
        T = set(form.cleaned_data['title'].lower())

        similar_meetings = []
        for meeting in models.Meeting.objects.all():
            S = set(meeting.title.lower())
            similarity = len(S & T) / len(S | T)
            if similarity > threshold:
                similar_meetings.append(meeting)

        return similar_meetings

    def meeting_unique(self, form):
        self.save_workflow_data(form)
        return super(CheckForSimilarMeetingsView, self).form_valid(form)

    def meeting_duplicate(self, form, similar_meetings):
        form.helper.layout.fields[1].fields[0].value = "Continue Anyway"
        form.helper.layout.fields.append(Hidden('bypass_check', ''))
        return self.render_to_response(
            self.get_context_data(form=form,
                                  similar_meetings=similar_meetings))

    def form_valid(self, form):
        if 'bypass_check' in self.request.POST:
            return self.meeting_unique(form)

        similar_meetings = self.check_for_similar_meetings(form)
        if similar_meetings:
            return self.meeting_duplicate(form, similar_meetings)
        else:
            return self.meeting_unique(form)

    def save_workflow_data(self, form):
        self.request.session['create_meeting-workflow'] = form.cleaned_data


@LoginRequired
class CreateMeetingInfoView (views.CreateView):
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
        return super(CreateMeetingInfoView, self).get_form_kwargs()

@LoginRequired
class UpdateMeetingInfoView (views.UpdateView):
    model = models.Meeting
    form_class = forms.FillInMeetingInfoForm
    template_name = 'edit_meeting-fill_info.html'

    def get_success_url(self):
        return reverse('browse_meetings_meeting_detail', kwargs={'slug': self.object.slug})

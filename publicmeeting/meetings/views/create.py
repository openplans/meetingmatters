from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views
from taggit import models as taggit_models

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

    def form_valid(self, form):
        self.save_workflow_data(form)
        return super(CheckForSimilarMeetingsView, self).form_valid(form)

    def save_workflow_data(self, form):
        self.request.session['create_meeting-workflow'] = form.cleaned_data


@LoginRequired
class FillInMeetingInfoView (views.CreateView):
    model = models.Meeting
    form_class = forms.FillInMeetingInfoForm
    template_name = 'create_meeting-fill_info.html'

    def get_success_url(self):
        return reverse('browse_meetings_meeting_detail', kwargs={'slug': self.object.slug})

    def get_workflow_data(self):
        workflow_data = self.request.session.get('create_meeting-workflow')
        return workflow_data or {}

    def get_form_kwargs(self):
        self.object = models.Meeting(**self.get_workflow_data())
        return super(FillInMeetingInfoView, self).get_form_kwargs()

@LoginRequired
class ModifyMeetingInfoView (views.UpdateView):
    model = models.Meeting
    form_class = forms.FillInMeetingInfoForm
    template_name = 'create_meeting-fill_info.html'

    def get_success_url(self):
        return reverse('browse_meetings_meeting_detail', kwargs={'slug': self.object.slug})

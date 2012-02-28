from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views

from project.utils.decorators import LoginRequired

from .. import forms
from .. import models

@LoginRequired
class CheckForSimilarMeetingsView (views.FormView):
    form_class = forms.CheckForSimilarMeetingsForm
    template_name = 'create_meeting-search_similar.html'

    def get_success_url(self):
        return reverse('create_meeting_fill_info')



@LoginRequired
class FillInMeetingInfoView (views.FormView):
    form_class = forms.FillInMeetingInfoForm
    template_name = 'create_meeting-fill_info.html'

    def get_success_url(self):
        return reverse('browse_meetings_meeting_detail', kwargs={'slug': self.meeting.slug})

    def get_initial(self):
        return self.request.GET

    def form_valid(self, form):
        self.meeting = form.save()
        return super(FillInMeetingInfoView, self).form_valid(form)

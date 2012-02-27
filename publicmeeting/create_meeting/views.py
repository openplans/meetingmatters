from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views

from . import forms

class CheckForSimilarMeetingsView (views.FormView):
    form_class = forms.CheckForSimilarMeetingsForm
    template_name = 'create_meeting-search_similar.html'
    
    def get_success_url(self):
    	return reverse('create_meeting_fill_info')


class FillInMeetingInfoView (views.FormView):
    form_class = forms.FillInMeetingInfoForm
    template_name = 'create_meeting-fill_info.html'
    
    def get_success_url(self):
    	return '/meetings/create/finish'

    def get_initial(self):
    	return self.request.GET

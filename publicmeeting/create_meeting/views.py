from django.views import generic as views

from . import forms

class CheckForSimilarMeetingsView (views.FormView):
    form_class = forms.CheckForSimilarMeetingsForm
    template_name = 'create_meeting-search_similar.html'
    success_url = '/meetings/create/step2'


class FillInMeetingInfoView (views.FormView):
    form_class = forms.FillInMeetingInfoForm
    template_name = 'create_meeting-fill_info.html'
    success_url = '/meetings/create/finish'

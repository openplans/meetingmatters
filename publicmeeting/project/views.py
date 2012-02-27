from django.views import generic as views

from . import models

class MeetingListView (views.ListView):
    model = models.Meeting
    context_object_name = 'meetings'
    template_name = 'browse_meetings-meeting_list.html'


class MeetingDetailView (views.DetailView):
    model = models.Meeting
    context_object_name = 'meeting'
    template_name = 'browse_meetings-meeting_detail.html'
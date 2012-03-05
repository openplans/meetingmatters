from django.views import generic as views
from taggit import models as taggit_models

from .. import models

class MeetingListView (views.ListView):
    model = models.Meeting
    context_object_name = 'meetings'
    template_name = 'browse_meetings-meeting_list.html'

    def get_context_data(self, **kwargs):
        context = super(MeetingListView, self).get_context_data(**kwargs)

        tag_slugs = self.request.GET.getlist('tags')
        context['tags'] = taggit_models.Tag.objects.all().order_by('name')
        context['selected_tags'] = taggit_models.Tag.objects.filter(slug__in=tag_slugs)

        return context

    def get_queryset(self):
        queryset = models.Meeting.objects.all().order_by('-begin_time')
        tag_slugs = self.request.GET.getlist('tags')

        if tag_slugs:
            queryset = queryset.filter(tags__slug__in=tag_slugs).distinct()

        return queryset


class MeetingDetailView (views.DetailView):
    model = models.Meeting
    context_object_name = 'meeting'
    template_name = 'browse_meetings-meeting_detail.html'

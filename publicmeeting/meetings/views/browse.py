from django.core.urlresolvers import reverse
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
        queryset = models.Meeting.objects.all().order_by('-begin_time').select_related()
        tag_slugs = self.request.GET.getlist('tags')

        if tag_slugs:
            for tag_slug in tag_slugs:
                queryset = queryset.filter(tags__slug=tag_slug)
        queryset.distinct()

        return queryset


class MeetingDetailView (views.DetailView):
    model = models.Meeting
    context_object_name = 'meeting'
    template_name = 'browse_meetings-meeting_detail.html'

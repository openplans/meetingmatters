from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views
from datetime import datetime

from meetings.models import Meeting
from meetings.models import Region
from meetings.views.browse import MeetingListMixin
from meetings.views.browse import DefaultMeetingFilters


class AboutView (views.TemplateView):
    template_name = 'project-about.html'


class HomepageView (MeetingListMixin, views.TemplateView):
    template_name = 'project-home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        filters = self.request.session.get('default_filters', {})
        meetings = self.get_meetings(**filters)
        meetings = meetings.filter(begin_time__gt=datetime.now())
        meetings = meetings.order_by('begin_time')

        context['meetings'] = meetings
        if filters.get('region'):
            try:
                context['region'] = Region.objects.get(slug=filters['region'])
            except Region.DoesNotExist:
                pass
        return context


class RegionSetterView (views.View):

    def get(self, request, *args, **kwargs):
        region = request.GET.get('region', None)
        next = request.GET.get('next', reverse('project-home'))
        default_filters = self.request.session.get('default_filters', {})

        if region:
            default_filters['region'] = region
        elif 'region' in default_filters:
            del default_filters['region']
        request.session['default_filters'] = default_filters

        return HttpResponseRedirect(next)

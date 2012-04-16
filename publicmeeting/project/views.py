from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic as views
from datetime import date, datetime

from meetings.forms import MeetingFilters
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
        form = MeetingFilters(data=filters)
        if form.is_valid():
            context['region'] = form.cleaned_data.get('region')
            form.cleaned_data.update({'earliest': date.today()})
            context['meetings'] = self.get_meetings(**form.cleaned_data)
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

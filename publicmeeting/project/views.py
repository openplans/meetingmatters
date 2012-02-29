from django.views import generic as views
from datetime import datetime

from meetings.models import Meeting

class HomepageView (views.TemplateView):
    template_name='project-home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        context['meetings'] = Meeting.objects.filter(begin_time__gt=datetime.now()).order_by('begin_time')
        return context

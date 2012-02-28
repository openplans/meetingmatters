from django.conf.urls.defaults import patterns, include, url

from .. import views

urlpatterns = patterns('create_meeting',
    url(r'^meetings/$', views.MeetingListView.as_view(),
        name='browse_meetings_meeting_list'),
    url(r'^meetings/(?P<slug>.+)$', views.MeetingDetailView.as_view(),
        name='browse_meetings_meeting_detail'),
)

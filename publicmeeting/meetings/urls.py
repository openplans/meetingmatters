from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('meetings',
    # Browse
    url(r'^$', views.MeetingListView.as_view(),
        name='browse_meetings_meeting_list'),
    url(r'^(?P<slug>.+)$', views.MeetingDetailView.as_view(),
        name='browse_meetings_meeting_detail'),

    # Create
    url(r'^meetings/create/$', views.CheckForSimilarMeetingsView.as_view(),
    	name='create_meeting_search_similar'),
    url(r'^meetings/create/step2$', views.FillInMeetingInfoView.as_view(),
    	name='create_meeting_fill_info'),
)

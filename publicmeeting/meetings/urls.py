from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('meetings',
    # Create
    url(r'^create/$', views.CheckForSimilarMeetingsView.as_view(),
    	name='create_meeting_search_similar'),
    url(r'^create/step2$', views.FillInMeetingInfoView.as_view(),
    	name='create_meeting_fill_info'),

    # Browse
    url(r'^$', views.MeetingListView.as_view(),
        name='browse_meetings_meeting_list'),
    url(r'^(?P<slug>[^/]+)/$', views.MeetingDetailView.as_view(),
        name='browse_meetings_meeting_detail'),

    # Edit
    url(r'^(?P<slug>.+)/edit/$', views.ModifyMeetingInfoView.as_view(),
        name='edit_meeting_change_info'),
)

from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('meetings',
    # Create
    url(r'^create/$', views.CheckForSimilarMeetingsView.as_view(),
    	name='create_meeting_search_similar'),
    url(r'^create/step2$', views.CreateMeetingInfoView.as_view(),
    	name='create_meeting_fill_info'),

    # Browse
    url(r'^$', views.MeetingListView.as_view(),
        name='browse_meetings_meeting_list'),
    url(r'^\?tags=(?P<slug>[^&]+)$', views.MeetingListView.as_view(),
        name='browse_meetings_meeting_by_tag'),
    url(r'^(?P<slug>[^/]+)/$', views.MeetingDetailView.as_view(),
        name='browse_meetings_meeting_detail'),

    # Update
    url(r'^(?P<slug>.+)/edit/$', views.UpdateMeetingInfoView.as_view(),
        name='update_meeting_fill_info'),
)

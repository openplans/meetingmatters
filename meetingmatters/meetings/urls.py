from django.conf.urls.defaults import patterns, include, url

from . import feeds
from . import views

urlpatterns = patterns('meetings',
    # Create
    url(r'^create/$', views.CheckForSimilarMeetingsView.as_view(),
    	name='create_meeting_search_similar'),
    url(r'^create/step2$', views.CreateMeetingInfoView.as_view(),
    	name='create_meeting_fill_info'),
    url(r'^venue/create/$', views.CreateVenueInfoView.as_view(),
      name='meetings_create_venue'),

    # Browse
    url(r'^$', views.MeetingListView.as_view(),
        name='browse_meetings_meeting_list'),
    url(r'^listpartial$', views.MeetingListPartialView.as_view(),
        name='browse_meetings_meeting_list_partial'),
    url(r'^~(?P<slug>[^/]+)/$', views.MeetingDetailView.as_view(),
        name='browse_meetings_meeting_detail'),

    # Update
    url(r'^(?P<slug>.+)/edit/$', views.UpdateMeetingInfoView.as_view(),
        name='update_meeting_fill_info'),

    # Feeds
    url(r'^rss/$', feeds.MeetingListRss(),
        name='meeting_list_rss'),
    url(r'^ical/$', feeds.MeetingListICal(),
        name='meeting_list_ical'),

    # API
    url(r'^api/v1/meetings/$', views.MeetingListApiView.as_view(),
        name='meeting_list_resource')
)

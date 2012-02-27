from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('create_meeting',
    url(r'^create/$', views.CheckForSimilarMeetingsView.as_view(),
    	name='create_meeting_search_similar'),
    url(r'^create/step2$', views.FillInMeetingInfoView.as_view(),
    	name='create_meeting_fill_info'),
)

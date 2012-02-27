from django.conf.urls.defaults import patterns, include, url

from django.views.generic import TemplateView

from . import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'publicmeeting.views.home', name='home'),
    # url(r'^publicmeeting/', include('publicmeeting.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('social_auth.urls')),
    url(r'', include('django.contrib.auth.urls')),

    url(r'^meetings/', include('create_meeting.urls')),

    url(r'^meetings/$', views.MeetingListView.as_view(),
        name='browse_meetings_meeting_list'),
    url(r'^meetings/(?P<slug>.+)$', views.MeetingDetailView.as_view(),
        name='browse_meetings_meeting_detail'),

    url(r'^$', TemplateView.as_view(template_name='project-home.html')),
)

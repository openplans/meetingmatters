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

    url(r'^s/', include('shorturls.urls')),
    url(r'^meetings/', include('meetings.urls')),
    url(r'^utils/', include('utils.urls')),

    url(r'^$', views.HomepageView.as_view(),
        name='project-home'),
    url(r'^choose-region/$', views.DefaultMeetingFilters.as_view(),
        name='project-choose_region'),
    url(r'^about/$', views.AboutView.as_view(),
        name='project-about'),
    url(r'^set-region/$', views.RegionSetterView.as_view(),
        name='set-region'),
)

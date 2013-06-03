from django.conf.urls.defaults import patterns, include, url

from . import views

urlpatterns = patterns('utils',
    # Geo
    url(r'^geoautocomplete/$', views.GeoAutocomplete.as_view(),
    	name='utils_geoautocomplete'),
)

import sys

from django.conf import settings as django_settings
from django.contrib.sites.models import Site
from django.core.cache import cache

from meetings import models

def regions(request):
    regions = cache.get('regions')
    
    if regions is None:
        regions = list(models.Region.objects.all())
        cache.set('regions', regions)
    
    default_filters = request.session.get('default_filters', {})
    region_slug = default_filters.get('region', None)

    current_region = None
    if region_slug:
        for region in regions:
            if region.slug == region_slug:
                current_region = region
                region.is_current = True

    return { 'regions': regions,
             'current_region': current_region }

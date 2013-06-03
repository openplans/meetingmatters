import sys

from django.conf import settings as django_settings
from django.contrib.sites.models import Site


###############################################################################
#
# Settings
#

# Add processors in the settings like so:
#
# TEMPLATE_CONTEXT_PROCESSORS = (
#     ...
#     'utils.context_processors.settings.<SETTING_NAME>',
# )
#
# Then <SETTING_NAME> will automagically show up in our template contexts!
#

class SettingsProcessor(object):
    def __getattr__(self, attr):
        if attr == '__file__':
            # autoreload support in dev server
            return __file__
        else:
            return lambda request: { attr: getattr(django_settings, attr) }

sys.modules[__name__ + '.settings'] = SettingsProcessor()


###############################################################################
#
# Site
#

def site(request):
    return { 'site': Site.objects.get_current() }

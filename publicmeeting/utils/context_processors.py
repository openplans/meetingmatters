import sys

from django.conf import settings as django_settings

class SettingsProcessor(object):
    def __getattr__(self, attr):
        if attr == '__file__':
            # autoreload support in dev server
            return __file__
        else:
            return lambda request: {attr: getattr(django_settings, attr)}

# With the following line, we can add processors in the settings like so:
#
# TEMPLATE_CONTEXT_PROCESSORS = (
#     ...
#     'utils.context_processors.settings.<SETTING_NAME>',
# )
#
# Then <SETTING_NAME> will automagically show up in our template contexts!
#
sys.modules[__name__ + '.settings'] = SettingsProcessor()

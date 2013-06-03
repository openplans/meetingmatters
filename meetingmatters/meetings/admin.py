from django.contrib import admin
from reversion import VersionAdmin
from . import models

class MeetingAdmin (VersionAdmin):
    pass

admin.site.register(models.Meeting, MeetingAdmin)
admin.site.register(models.MeetingTopic)
admin.site.register(models.Venue)

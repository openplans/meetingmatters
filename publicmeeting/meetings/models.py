from __future__ import division
#from django.contrib.gis.db import models
from django.db import models
from taggit.managers import TaggableManager

from utils.models import TimestampedModelMixin, SlugifiedModelMixin


class Meeting (SlugifiedModelMixin, TimestampedModelMixin, models.Model):
    title = models.CharField(max_length=1023, verbose_name="Meeting Name", help_text="The meeting name should be descriptive. What makes a good meeting name? What makes a bad one?")
    """The title of the meeting"""

    description = models.TextField(null=True, blank=True, help_text="Give readers an idea of the purpose of the meeting, as well as what will be discussed. If there is an agenda, include that as well.")
    """The meeting description, potentially including the agenda."""

    begin_time = models.DateTimeField(null=True, blank=True, verbose_name="Start time")
    """When does the meeting start.  NULL means TBD."""

    end_time = models.DateTimeField(null=True, blank=True, verbose_name="End time")
    """When does the meeting end.  NULL means ???."""

    venue_name = models.TextField(null=True, blank=True, verbose_name="Venue Address")
    """The name or address of the venue.  NULL means TBD."""

#    venue_location = models.PointField(null=True, blank=True)
#    """The geographical location of the venue.  NULL means TBD."""

    venue_additional = models.TextField(null=True, blank=True, verbose_name="Notes")
    """Additional information about the venue, such as room number."""

    tags = TaggableManager(blank=True, verbose_name="Topics", help_text="A comma-separated list of topics that will be discussed at the meeting.")
    """The tags for the meeting"""

    speakers = models.ManyToManyField('auth.User', related_name='speaking_meetings', blank=True)
    attendees = models.ManyToManyField('auth.User', related_name='attending_meetings', blank=True)
    """Who is attending and/or speaking at the meeting"""

#    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('browse_meetings_meeting_detail', [str(self.slug)])

    def get_pre_slug(self):
        return self.title

    def similar_meetings(self, threshold=0.7):
        T = set(self.title.lower())

        similar_meetings = []
        for meeting in Meeting.objects.all():
            S = set(meeting.title.lower())
            similarity = len(S & T) / len(S | T)
            if similarity > threshold:
                similar_meetings.append(meeting)

        return similar_meetings

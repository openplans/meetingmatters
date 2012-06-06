from __future__ import division
#from django.contrib.gis.db import models
from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.core.cache import cache
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from utils.geocode import geocode
from utils.models import TimestampedModelMixin, SlugifiedModelMixin


class CachingManager (models.Manager):
    def get_cache_key(self):
        opts = self.model._meta
        return '.'.join([opts.app_label, opts.module_name])

    def cached(self):
        key = self.get_cache_key()
        topics = cache.get(key)

        if topics is None:
            topics = self.all()
            cache.set(key, topics)

        return topics

    def bust_cache(self):
        key = self.get_cache_key()
        cache.delete(key)


class Region (SlugifiedModelMixin, TimestampedModelMixin, models.Model):
    """A general region in which meetings take place"""

    name = models.CharField(max_length=256)
    """The name of this region"""

    def __unicode__(self):
        return self.name

    objects = CachingManager()


class Venue (SlugifiedModelMixin, TimestampedModelMixin, models.Model):
    """A venue where meetings take place"""

    name = models.CharField(max_length=256, null=True, blank=True)
    """The name of the venue"""

    address = models.CharField(max_length=1024)
    """The address of the venue"""

    location = models.PointField(blank=True)
    """A geographical point representing the venue"""

    objects = models.GeoManager()

    def get_pre_slug(self):
        return self.name or self.address

    def __unicode__(self):
        if self.name:
            return "{n}, {a}".format(n=self.name, a=self.address)
        else:
            return self.address

    objects = CachingManager()

    def save(self, *args, **kwargs):
        if self.location is None:
            geo = geocode(self.address)
            if not geo or not geo['results']:
                raise models.FieldError('Cannot find address')
            geo = geo['results'][0]
            self.location = geos.Point(
                geo['geometry']['location']['lng'],
                geo['geometry']['location']['lat'])
        super(Venue, self).save(*args, **kwargs)


class MeetingTopicManager (CachingManager):
    def all(self):
        return super(MeetingTopicManager, self).all().order_by('name')


class MeetingTopic (SlugifiedModelMixin, models.Model):
    name = models.CharField(verbose_name='Topic', max_length=100)

    # meetings (reverse)

    objects = CachingManager()
    ordered_objects = MeetingTopicManager()

    def __unicode__(self):
        return self.name

    def get_pre_slug(self):
        return self.name

    def save(self, *args, **kwargs):
        super(MeetingTopic, self).save(*args, **kwargs)
        MeetingTopic.objects.bust_cache()


class Meeting (SlugifiedModelMixin, TimestampedModelMixin, models.Model):
    title = models.CharField(max_length=1023, verbose_name="Meeting Name", help_text="The meeting name should be descriptive. What makes a good meeting name? What makes a bad one?")
    """The title of the meeting"""

    description = models.TextField(null=True, blank=True, help_text="Give readers an idea of the purpose of the meeting, as well as what will be discussed. If there is an agenda, include that as well.")
    """The meeting description, potentially including the agenda."""

    begin_time = models.DateTimeField(null=True, blank=True, verbose_name="Start time")
    """When does the meeting start.  NULL means TBD."""

    end_time = models.DateTimeField(null=True, blank=True, verbose_name="End time")
    """When does the meeting end.  NULL means ???."""

    region = models.ForeignKey('Region', null=True, verbose_name="Region")
    """The region in which this meeting takes place"""

    venue = models.ForeignKey('Venue', null=True, blank=True, related_name='meetings')
    """The venue where the meeting will take place"""

    venue_name = models.TextField(null=True, blank=True, verbose_name="Venue Address")
    """The name or address of the venue.  NULL means TBD."""

#    venue_location = models.PointField(null=True, blank=True)
#    """The geographical location of the venue.  NULL means TBD."""

    venue_additional = models.TextField(null=True, blank=True, verbose_name="Notes")
    """Additional information about the venue, such as room number."""

    tags = models.ManyToManyField('MeetingTopic', related_name='meetings', blank=True, verbose_name="Topics", help_text="A comma-separated list of topics that will be discussed at the meeting.")
    """The tags for the meeting"""

    speakers = models.ManyToManyField('auth.User', related_name='speaking_meetings', blank=True)
    attendees = models.ManyToManyField('auth.User', related_name='attending_meetings', blank=True)
    """Who is attending and/or speaking at the meeting"""

    canceled = models.BooleanField(default=False, blank=True)
    """Whether the meeting is canceled"""

    # Meeting has no geo fields, but we want to be able to do geo queries on
    # meetings, so we need a GeoManager.
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('browse_meetings_meeting_detail', [str(self.slug)])

    def get_pre_slug(self):
        return self.title

    # It takes "a long time" to get the tags for each meeting in a meeting list,
    # so we're going to do some simple caching.
    def get_cached_tags(self):
        if self.pk is None:
            return []

        cache_key = 'tags_' + str(self.pk)
        tags = cache.get(cache_key)
        if tags is None:
            tags = self.tags.all()
            cache.set(cache_key, tags)

        return tags

    def bust_tag_cache(self):
        cache_key = 'tags_' + str(self.pk)
        cache.delete(cache_key)

    def similar_meetings(self, threshold=0.7):
        T = set(self.title.lower())
        all_meetings = Meeting.objects.all()

        if self.region:
            all_meetings = all_meetings.filter(region = self.region)

        similar_meetings = []
        for meeting in all_meetings:
            S = set(meeting.title.lower())
            similarity = len(S & T) / len(S | T)
            if similarity > threshold:
                similar_meetings.append(meeting)

        return similar_meetings

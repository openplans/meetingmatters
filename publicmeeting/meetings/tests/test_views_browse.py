from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from taggit.models import Tag
from nose.tools import *

from meetings.models import Meeting, Venue
from meetings.views.browse import MeetingListView

class Test_MeetingListView:

    def setup(world):
        Meeting.objects.all().delete()
        Tag.objects.all().delete()
        Venue.objects.all().delete()

        world.url = reverse('browse_meetings_meeting_list')
        world.client = Client()
        world.client.login(username='blah', password='cool')

    @istest
    def returns_only_meetings_with_the_specified_tags (world):
        t1 = Tag.objects.create(name='t1')
        t2 = Tag.objects.create(name='t2')
        t3 = Tag.objects.create(name='t3')

        m1 = Meeting.objects.create(slug='m1'); m1.tags.add(t1)
        m2 = Meeting.objects.create(slug='m2'); m2.tags.add(t2)
        m3 = Meeting.objects.create(slug='m3'); m3.tags.add(t3)

        response = world.client.get(world.url + '?tags=t1&tags=t3')
        assert_equal(set(response.context['meetings']), set([m1, m3]))

    @istest
    def returns_meetings_within_the_radius_of_a_given_point (world):
        p1 = Point(12.34, 56.78)
        p2 = Point(87.65, 43.21)

        v1 = Venue.objects.create(location=p1)
        v2 = Venue.objects.create(location=p2)

        m1 = Meeting.objects.create(slug='m1', title='meeting 1', venue=v1)
        m2 = Meeting.objects.create(slug='m2', title='meeting 2', venue=v2)

        response = world.client.get(world.url + '?center=POINT(12.34 56.78)&radius=1.0')
        assert_equal(list(response.context['meetings']), [m1])

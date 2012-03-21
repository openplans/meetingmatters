from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from taggit.models import Tag
from nose.tools import *

from meetings.models import Meeting
from meetings.views.browse import MeetingListView

class Test_MeetingListView:

    def setup(world):
        world.url = reverse('browse_meetings_meeting_list')

        Meeting.objects.all().delete()
        Tag.objects.all().delete()

        t1 = Tag.objects.create(name='t1')
        t2 = Tag.objects.create(name='t2')
        t3 = Tag.objects.create(name='t3')

        world.client = Client()
        world.client.login(username='blah', password='cool')

    @istest
    def correctly_sets_the_querystring_for_toggling_tags (world):
        # Query for tag1
        response = world.client.get(world.url + '?tags=t1')

        for tag in response.context['tags']:
            # The querystring for tag1 should turn it off.
            if tag.name == 't1':
                assert_equal(tag.qs, '')

            # The querystring for any other tag should turn that tag on, and
            # leave tag1 on.
            else:
                assert_equal(tag.qs, 'tags=t1&tags=' + tag.slug)

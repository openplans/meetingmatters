from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from nose.tools import *

from meetings.views.create import CheckForSimilarMeetingsView

class Test_CheckForSimilarMeetingsView:

    @istest
    def can_only_be_accessed_by_authenticated_user (self):
        url = reverse('create_meeting_search_similar')
        client = Client()

        client.logout()
        response = client.get(url)
        assert_equal(
            response.status_code,
            302
        )

        User.objects.all().delete()
        User.objects.create_user(username='blah', password='cool')
        client.login(username='blah', password='cool')
        response = client.get(url)
        assert_equal(
            response.status_code,
            200
        )


class Test_FillInMeetingInfoView:

    def setup (world):
        world.url = reverse('create_meeting_fill_info')
        User.objects.all().delete()

        world.credentials = dict(username='blah', password='cool')
        User.objects.create_user(**world.credentials)

    @istest
    def can_only_be_accessed_by_authenticated_user (world):
        client = Client()

        client.logout()
        response = client.get(world.url)
        assert_equal(
            response.status_code,
            302
        )

        client.login(**world.credentials)
        response = client.get(world.url)
        assert_equal(
            response.status_code,
            200
        )

    @istest
    def retrieves_initial_information_from_the_session (world):
        client = Client()

        client.login(**world.credentials)

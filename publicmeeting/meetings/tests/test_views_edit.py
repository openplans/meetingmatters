from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from nose.tools import *

from meetings.models import Meeting
from meetings.views.create import CheckForSimilarMeetingsView

class Test_CheckForSimilarMeetingsView:

    def setup(world):
        world.url = reverse('create_meeting_search_similar')

        Meeting.objects.all().delete()
        User.objects.all().delete()
        User.objects.create_user(username='blah', password='cool')

        world.client = Client()
        world.client.login(username='blah', password='cool')

    @istest
    def can_only_be_accessed_by_authenticated_user (world):
        # First try with logged in user.
        response = world.client.get(world.url)
        assert_equal(
            response.status_code,
            200
        )

        # Now log out and try again.
        world.client.logout()
        response = world.client.get(world.url)
        assert_equal(
            response.status_code,
            302
        )

    @istest
    def renders_self_on_POST_if_similar_meetings_found (world):
        # Create a "pre-existing" meeting.
        Meeting.objects.create(title='My New Meeting')

        # Try to post with a new similar meeting.
        response = world.client.post(
            world.url,
            {'title': 'my new meeting'}
        )

        # The page should not have redirected.
        assert_equal(
            response.status_code,
            200
        )

    @istest
    def redirects_on_POST_if_form_is_valid_an_no_similar_meetings_found (world):
        # Create a "pre-existing" meeting.
        Meeting.objects.create(title='My New Meeting')

        # Try to post with a dissimilar meeting.
        response = world.client.post(
            world.url,
            {'title': 'Crazy Stuff!'}
        )

        # The page should have redirected.
        assert_equal(
            response.status_code,
            302
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

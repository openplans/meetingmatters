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

    @istest
    def can_only_be_accessed_by_authenticated_user (self):
        url = reverse('create_meeting_fill_info')
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

from django.test import TestCase
from nose.tools import *

from meetings.models import Meeting

class Test_Meeting:

    def setup(self):
        Meeting.objects.all().delete()

    @istest
    def has_slug_on_save (self):
        Meeting.objects.all().delete()
        instance = Meeting(title='hello, world!')
        instance.save()

        assert_equal(
            instance.slug,
            'hello-world'
        )

    @istest
    def similarMeetings_matches_two_meetings_with_similar_names (world):
        # If this test is failing, remember to import division from __future__
        # wherever you're calculating the similarity.

        stored_meeting = Meeting.objects.create(title='My New Meeting')
        meeting = Meeting(title='my newest meeting')

        assert_equal(
            meeting.similar_meetings(),
            [stored_meeting]
        )

    @istest
    def similarMeetings_does_not_match_two_meetings_with_dissimilar_names (world):
        stored_meeting = Meeting.objects.create(title='My New Meeting')
        meeting = Meeting(title='Strange Other One')

        assert_equal(
            meeting.similar_meetings(),
            []
        )

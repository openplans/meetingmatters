from django.test import TestCase
from nose.tools import *

from meetings.models import Meeting

class Test_Meeting:

    @istest
    def has_slug_on_save (self):
        Meeting.objects.all().delete()
        instance = Meeting(title='hello, world!')
        instance.save()

        assert_equal(
            instance.slug,
            'hello-world'
        )

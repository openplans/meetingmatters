from django.test import TestCase
from nose.tools import *

from utils import slugify_uniquely

class Test_slugifyUniquely:
    def setUp (self):
        class QuerySetStub (object):
            def __init__(self, count=0):
                self.__count = count

            def count(self):
                return self.__count

        class ModelManagerStub (object):
            def filter(self, slug=None):
                if slug in (
                    'this-is-another',
                    'this-is-anoth-2',
                    'this-is-anoth-3',

                    'this', 'thi-2',
                    'thi-3', 'thi-4',
                    'thi-5', 'thi-6',
                    'thi-7', 'thi-8',
                    'thi-9', 'th-10',

                    'surprise',
                    'surprise-2',
                    'surprise-3'):
                    return QuerySetStub(count=1)
                return QuerySetStub(count=0)

        class ModelStub (object):
            objects = ModelManagerStub()

        self.Model = ModelStub
        self.instance = ModelStub()

    @istest
    def truncates_long_strings (self):
        assert_equal(
            slugify_uniquely('This is a Test', self.Model, 12),
            'this-is-a-te'
        )

    @istest
    def doesnt_truncate_short_strings (self):
        assert_equal(
            slugify_uniquely('Surprise!', self.Model, 20),
            'surprise-4'
        )

    @istest
    def increments_slug_suffix (self):
        assert_equal(
            slugify_uniquely('This is another Test', self.Model, 15),
            'this-is-anoth-4'
        )

    @istest
    def supports_2_digit_slug_suffixes (self):
        assert_equal(
            slugify_uniquely('This', self.Model, 5),
            'th-11'
        )

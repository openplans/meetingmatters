#!/usr/bin/env python

from distutils.core import setup
import os

def get_packages(*package_roots):
    """
    Return root package and all sub-packages.
    """
    packages = []
    for package in package_roots:
        packages += [dirpath
                     for dirpath, dirnames, filenames in os.walk(package)
                     if os.path.exists(os.path.join(dirpath, '__init__.py'))]
    return packages


def get_package_data(*package_roots):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    package_data = {}
    for package in package_roots:
        walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
                for dirpath, dirnames, filenames in os.walk(package)
                if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

        filepaths = []
        for base, filenames in walk:
            filepaths.extend([os.path.join(base, filename)
                              for filename in filenames])
        package_data[package] = filepaths
    return package_data


setup(
    name='meetingmatters',
    version='1.0',
    description='Meeting and event management Django app',
    author='OpenPlans',
    author_email='hellp@openplans.org',
    url='http://github.com/openplans/meetingmatters',
    packages=get_packages('meetingmatters'),
    package_data=get_package_data('meetingmatters'),
    dependency_links=[
        'git+git://github.com/statesofpop/django-cal.git#egg=django-cal-dev',
        'git+git://github.com/mjumbewu/django-bootstrapped.git@bootstrap2#egg=django-bootstrapped-1.0.3-dev',
    ],
    install_requires=[

        # Database (PostgreSQL)
        'psycopg2',

        # Revision management
        'django-reversion>=1.7',

        # Search
        'django-haystack',

        # Tagging
        'django-taggit',

        # Sharing
        'django-shorturls',
        'django-cal==dev',

        # Authentication
        'django-social-auth==0.7.22',

        # Async requests
        'djangorestframework',
#        'requests',
        'django-pjax',

        # Template and style helpers
        'django-bootstrapped==1.0.3-dev',
        'django-uni-form',
        'django-floppyforms',
        'django-taggit-templatetags',
        'django-compressor',
        'slimit',
        'django-templatetag-sugar',

        # Testing and debugging
        'django-nose',
        'django-debug-toolbar',

        # Time
        'pytz',

    ],
)

import datetime
import floppyforms as forms
import taggit.forms
import taggit.models
from django.contrib.gis import geos
from django.core.urlresolvers import reverse
from uni_form.helper import FormHelper
from uni_form.layout import Layout, ButtonHolder, Submit, Fieldset

from . import models
from utils.geocode import geocode

import logging
log = logging.getLogger(__name__)

class CheckForSimilarMeetingsForm (forms.Form):
    title = forms.CharField(
        label="Meeting Name",
        help_text="The meeting name should be descriptive. What makes a good meeting name? What makes a bad one?",
        widget=forms.TextInput(attrs={'class':'span6'})
    )
    begin_time = forms.SplitDateTimeField(
        label="Start time",
        input_time_formats=('%H:%M', '%I:%M %p'),
        required=False
    )
    end_time = forms.SplitDateTimeField(
        label="End time",
        input_time_formats=('%H:%M', '%I:%M %p'),
        required=False
    )

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Fieldset(
                'Step 0: Check whether meeting exists',
                'title', 'begin_time', 'end_time',
            ),
            ButtonHolder(
                Submit('check', 'Continue', css_class='btn btn-primary pull-right')
            )
        )
        return super(CheckForSimilarMeetingsForm, self).__init__(*args, **kwargs)


#
# We won't use the taggit tags, but the form fields are still useful.
#
from django.utils.translation import ugettext as _
from taggit.utils import parse_tags, edit_string_for_tags

class MeetingTopicWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags(models.MeetingTopic.objects.filter(id__in=value))
        return super(MeetingTopicWidget, self).render(name, value, attrs)


class MeetingTopicField(forms.CharField):
    widget = MeetingTopicWidget

    def clean(self, value):
        value = super(MeetingTopicField, self).clean(value)
        try:
            tag_names = parse_tags(value)
        except ValueError:
            raise forms.ValidationError(_("Please provide a comma-separated list of tags."))

        tags = []
        for tag_name in tag_names:
            tag, created = models.MeetingTopic.objects.get_or_create(name=tag_name)
            tags.append(tag.id)

        return tags


class FillInMeetingInfoForm (forms.ModelForm):
    begin_time = forms.SplitDateTimeField(
        label="Start time",
        input_time_formats=('%H:%M', '%I:%M %p')
    )
    end_time = forms.SplitDateTimeField(
        label="End time",
        input_time_formats=('%H:%M', '%I:%M %p')
    )
    venue = forms.ModelChoiceField(
        queryset=models.Venue.objects.all(),
        widget=forms.Select(attrs={'class':'span4'}),
        required=False,
        help_text='If you do not find the venue in the list, you can <a href="#create-venue-modal" data-toggle="modal">create</a> a new one.'
    )
    tags = MeetingTopicField(
        widget=MeetingTopicWidget(attrs={'class':'span6'}),
    )
#    venue_name = forms.CharField(
#        label="Name",
#        widget=forms.TextInput(attrs={'class':'span6'})
#    )
#    venue_address = forms.CharField(
#        label="Address",
#        widget=forms.TextInput(attrs={'class':'span5'})
#    )

    class Meta:
        model = models.Meeting
        exclude = ('speakers', 'attendees', 'slug', 'venue_name')
        widgets = {
            'title': forms.TextInput(attrs={'class':'span6'}),
            'description': forms.Textarea(attrs={'class':'span6'}),
            'region': forms.Select(attrs={'class':'span6'}),
            'venue': forms.Select(attrs={'class':'span4'}),
            'venue_additional': forms.Textarea(attrs={'class':'span6', 'rows':'3'}),
        }

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Fieldset(
                'Step 1: Fill in general information',
                'title', 'begin_time', 'end_time',
                'description', 'tags'
            ),
            Fieldset(
                'Step 2: Enter the location',
                'region', 'venue', 'venue_additional'
            ),
            ButtonHolder(
                Submit('check', 'Save', css_class='btn btn-primary pull-right')
            )
        )

#        if instance and instance.venue:
#            initial = initial or {}
#            initial.update({
#                'venue_name': instance.venue.name,
#                'venue_address': instance.venue.address
#            })

#        kwargs.update({'initial': initial, 'instance': instance})
        return super(FillInMeetingInfoForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(FillInMeetingInfoForm, self).save(*args, **kwargs)
        instance.bust_tag_cache()
        return instance


class DefaultFilters (forms.Form):
    region = forms.ModelChoiceField(
        queryset=models.Region.objects.all(),
        to_field_name='slug',
        widget=forms.HiddenInput(),
    )


class DatepickerInput (forms.DateInput):
    template_name = 'floppyforms/meetings_datepicker.html'


class GeoBBInput (forms.DateInput):
    template_name = 'floppyforms/meetings_bbmap_google.html'


class MeetingFilters (forms.Form):
    region = forms.ModelChoiceField(queryset=models.Region.objects.all(), to_field_name='slug', required=False, empty_label='All regions')
    center = forms.CharField(required=False)
    radius = forms.FloatField(required=False)
    bbox = forms.CharField(required=False, widget=GeoBBInput())
    earliest = forms.DateField(required=False, initial=datetime.date.today, widget=DatepickerInput())
    latest = forms.DateField(required=False, widget=DatepickerInput())
    tags = forms.ModelMultipleChoiceField(queryset=models.MeetingTopic.objects.all(), to_field_name='slug', required=False)

    def clean(self):
        cleaned_data = super(MeetingFilters, self).clean()
        center = cleaned_data.get('center')
        radius = cleaned_data.get('radius')

        # Center and radius must be set together
        if center and not radius:
            msg = u'Radius is required when center is specified.'
            self._errors['radius'] = self.error_class([msg])

        if radius and not center:
            msg = u'Center is required when radius is specified.'
            self._errors['center'] = self.error_class([msg])

        if center:
            try:
                center = cleaned_data['center'] = geos.fromstr(center)
            except geos.GEOSException:
                msg = u'Center is not a valid WKT point (see http://en.wikipedia.org/wiki/Well-known_text)'
                self._errors['center'] = self.error_class([msg])

        # N, S, E, and W must all be set together, or none at all.
        bbox = cleaned_data.get('bbox')
        if bbox:
            try:
                n, e, s, w = [float(val) for val in cleaned_data['bbox'].split(',')]
                bbox = u'POLYGON(({e} {n}, {e} {s}, {w} {s}, {w} {n}, {e} {n}))'.format(n=n, e=e, s=s, w=w)
            except ValueError:
                msg = u'Bbox must have exactly 4 comma-separated values.'
                self._errors['bbox'] = self.error_class([msg])
            else:
                cleaned_data['bbox'] = geos.fromstr(bbox)

        return cleaned_data


class VenueForm (forms.ModelForm):
    class Meta:
        model = models.Venue
        exclude = ['slug', 'location']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
#        self.helper.form_method = 'POST'
#        self.helper.form_action = ''
#        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False

#        self.helper.layout = Layout(
#            Fieldset(
#                'Step 1: Fill in general information',
#                'title', 'begin_time', 'end_time',
#                'description', 'tags'
#            ),
#            Fieldset(
#                'Step 2: Enter the location',
#                'region', 'venue', 'venue_additional'
#            ),
#            ButtonHolder(
#                Submit('check', 'Save', css_class='btn btn-primary pull-right')
#            )
#        )

        return super(VenueForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(VenueForm, self).clean(*args, **kwargs)

        address = cleaned_data.get('address')
        if self.instance.address != address:
            geo = geocode(address)

            if not geo or not geo['results']:
                raise forms.ValidationError('Could not find this address.')

            geo = geo['results'][0]
            self.instance.location = geos.Point(
                geo['geometry']['location']['lng'],
                geo['geometry']['location']['lat'])

        return cleaned_data

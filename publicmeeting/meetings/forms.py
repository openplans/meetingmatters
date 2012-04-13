from django import forms
from django.core.urlresolvers import reverse
from taggit import forms as taggit

from uni_form.helper import FormHelper
from uni_form.layout import Layout, ButtonHolder, Submit, Fieldset

from . import models

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


class FillInMeetingInfoForm (forms.ModelForm):
    begin_time = forms.SplitDateTimeField(
        label="Start time",
        input_time_formats=('%H:%M', '%I:%M %p')
    )
    end_time = forms.SplitDateTimeField(
        label="End time",
        input_time_formats=('%H:%M', '%I:%M %p')
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
            'tags': taggit.TagWidget(attrs={'class':'span6'}),
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


class DefaultFilters (forms.Form):
    region = forms.ModelChoiceField(
        queryset=models.Region.objects.all(),
        to_field_name='slug',
        widget=forms.HiddenInput(),
    )

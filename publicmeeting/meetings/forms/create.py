from django import forms
from django.core.urlresolvers import reverse
from taggit import forms as taggit

from uni_form.helper import FormHelper
from uni_form.layout import Layout, ButtonHolder, Submit, Fieldset

from .. import models

class CheckForSimilarMeetingsForm (forms.Form):
    title = forms.CharField(
        label="Meeting Name",
        help_text="The meeting name should be descriptive. What makes a good meeting name? What makes a bad one?",
        widget=forms.TextInput(attrs={'class':'span6'})
    )
    begin_time = forms.SplitDateTimeField(
        label="Start time",
        input_time_formats=('%H:%M', '%I:%M %p')
    )
    end_time = forms.SplitDateTimeField(
        label="End time",
        input_time_formats=('%H:%M', '%I:%M %p')
    )

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Fieldset(
                'Step 1: Check whether meeting exists',
                'title', 'begin_time', 'end_time',
            ),
            ButtonHolder(
                Submit('check', 'Next', css_class='btn btn-primary pull-right')
            )
        )
        return super(CheckForSimilarMeetingsForm, self).__init__(*args, **kwargs)


class FillInMeetingInfoForm (forms.ModelForm):
    title = forms.CharField(
        label="Meeting Name",
        help_text="The meeting name should be descriptive. What makes a good meeting name? What makes a bad one?",
        widget=forms.TextInput(attrs={'class':'span6'})
    )
    begin_time = forms.SplitDateTimeField(
        label="Start time",
        input_time_formats=('%H:%M', '%I:%M %p')
    )
    end_time = forms.SplitDateTimeField(
        label="End time",
        input_time_formats=('%H:%M', '%I:%M %p')
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class':'span6'}),
        help_text="Give readers an idea of the purpose of the meeting, as well as what will be discussed. If there is an agenda, include that as well.",
        required=False
    )
    tags = taggit.TagField(
        widget=taggit.TagWidget(attrs={'class':'span6'})
    )
    venue_name = forms.CharField(
        label="Venue Address",
        widget=forms.TextInput(attrs={'class':'span5'})
    )
    venue_additional = forms.CharField(
        label="Notes",
        widget=forms.Textarea(attrs={'class':'span6', 'rows':'3'}),
        required=False
    )

    class Meta:
        model = models.Meeting
        exclude = ('speakers', 'attendees', 'slug')

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Fieldset(
                'Step 2: Fill in general information',
                'title', 'begin_time', 'end_time',
                'description', 'tags'
            ),
            Fieldset(
                'Step 3: Enter the location',
                'venue_name', 'venue_additional'
            ),
            ButtonHolder(
                Submit('check', 'Next', css_class='btn btn-primary pull-right')
            )
        )
        return super(FillInMeetingInfoForm, self).__init__(*args, **kwargs)

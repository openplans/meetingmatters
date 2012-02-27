from django import forms
from django.core.urlresolvers import reverse

from uni_form.helper import FormHelper
from uni_form.layout import Layout, ButtonHolder, Submit, Fieldset

class CheckForSimilarMeetingsForm (forms.Form):
    name = forms.CharField(
        label="Meeting Name",
        help_text="The meeting name should be descriptive. What makes a good meeting name? What makes a bad one?",
        widget=forms.TextInput(attrs={'class':'span6'})
    )

    start_date = forms.DateField(
        label="Start Time"
    )
    start_time = forms.TimeField(
        label="",
        widget=forms.TextInput(attrs={'placeholder':'10:00 AM'}),
        input_formats=('%H:%M', '%I:%M %p')
    )

    end_date = forms.DateField(
        label="End Time"
    )
    end_time = forms.TimeField(
        label="",
        widget=forms.TextInput(attrs={'placeholder':'12:00 PM'}),
        input_formats=('%H:%M', '%I:%M %p')
    )

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_action = reverse('create_meeting_fill_info')
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Fieldset(
                'Step 1: Check whether meeting exists',
                'name', 'start_date', 'start_time',
                'end_date', 'end_time',
            ),
            ButtonHolder(
                Submit('check', 'Next', css_class='btn btn-large btn-primary pull-right')
            )
        )
        return super(CheckForSimilarMeetingsForm, self).__init__(*args, **kwargs)


class FillInMeetingInfoForm (forms.Form):
    name = forms.CharField(
        label="Meeting Name",
        help_text="The meeting name should be descriptive. What makes a good meeting name? What makes a bad one?",
        widget=forms.TextInput(attrs={'class':'span6'})
    )

    start_date = forms.DateField(
        label="Start Time"
    )
    start_time = forms.TimeField(
        label="",
        widget=forms.TextInput(attrs={'placeholder':'10:00 AM'}),
        input_formats=('%H:%M', '%I:%M %p')
    )

    end_date = forms.DateField(
        label="End Time"
    )
    end_time = forms.TimeField(
        label="",
        widget=forms.TextInput(attrs={'placeholder':'12:00 PM'}),
        input_formats=('%H:%M', '%I:%M %p')
    )

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Fieldset(
                'Step 2: Fill in general information',
                'name', 'start_date', 'start_time',
                'end_date', 'end_time',
            ),
            ButtonHolder(
                Submit('check', 'Next', css_class='btn btn-large btn-primary pull-right')
            )
        )
        return super(FillInMeetingInfoForm, self).__init__(*args, **kwargs)

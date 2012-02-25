from django import forms

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
        label=""
    )

    end_date = forms.DateField(
        label="End Time"
    )
    end_time = forms.TimeField(
        label=""
    )

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Fieldset(
                'Step 1: Identifying Information',
                'name', 'start_date', 'start_time',
                'end_date', 'end_time',
            ),
            ButtonHolder(
                Submit('check', 'Next', css_class='btn btn-large btn-primary pull-right')
            )
        )
        return super(CheckForSimilarMeetingsForm, self).__init__(*args, **kwargs)

class FillInMeetingInfoForm (forms.Form):
    name = forms.CharField(max_length=1024)
    start_date = forms.DateField()
    start_time = forms.TimeField()
    end_date = forms.DateField()
    end_time = forms.TimeField()

# data_collection/forms.py

from django import forms

class ConsentForm(forms.Form):
    consent = forms.BooleanField(
        label="I agree to the data collection and privacy policy.",
        required=True
    )

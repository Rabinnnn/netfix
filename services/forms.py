from django import forms

from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices='', ** kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding choices to fields
        if choices:
            self.fields['field'].choices = choices
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'


class RequestServiceForm(forms.Form):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter Service Address'}),
        required=True
    )
    hours_needed = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Hours Needed'}),
        required=True
    )

    def clean_hours_needed(self):
        hours = self.cleaned_data.get('hours_needed')
        if hours < 1:
            raise forms.ValidationError("Hours must be at least 1")
        return hours

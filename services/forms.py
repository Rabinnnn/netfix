from django import forms
import re
from users.models import Company
from django.core.exceptions import ValidationError
from django.utils.html import escape

class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_per_hour = forms.DecimalField(
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
        self.fields['price_per_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'
# 

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

    def clean_address(self):
        address = self.cleaned_data.get('address')

        # Strip any potential dangerous scripts or tags (XSS prevention)
        sanitized_address = self.sanitize_input(address)
        
        # Optionally, you can further check for certain dangerous patterns
        if re.search(r'<script|<\/script|on\w+\s*=', sanitized_address, re.IGNORECASE):
            raise ValidationError("Suspicious content detected. Please avoid using scripts or event handlers.")
        
        # Return sanitized address to prevent harmful content being stored
        return sanitized_address

    def clean_hours_needed(self):
        hours = self.cleaned_data.get('hours_needed')
        
        # Define reasonable limits for hours (e.g., 1 to 1000 hours).
        MIN_HOURS = 1
        MAX_HOURS = 1000
        
        if hours < MIN_HOURS:
            raise forms.ValidationError(f"Hours must be at least {MIN_HOURS}")
        
        if hours > MAX_HOURS:
            raise forms.ValidationError(f"Hours must not exceed {MAX_HOURS}")
        
        return hours


    def sanitize_input(self, input_string):
        # Use Django's escape function to escape HTML special characters.
        # This ensures that any HTML or JavaScript is rendered as text and not executable.
        sanitized_input = escape(input_string)

        # Optionally, further clean the string by removing other unwanted characters or patterns.
        sanitized_input = self.remove_unwanted_characters(sanitized_input)

        return sanitized_input

    def remove_unwanted_characters(self, input_string):
        # Remove unwanted characters (like angle brackets or anything that can be part of an attack)
        input_string = re.sub(r'<.*?>', '', input_string)  # Remove all HTML tags
        
        # You can extend this further to remove other unwanted patterns if needed
        return input_string

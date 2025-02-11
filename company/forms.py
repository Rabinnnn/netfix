from django import forms
from .models import Service

class CreateNewService(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'field', 'price_per_hour']
#do


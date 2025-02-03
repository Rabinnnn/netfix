from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
import re

from .models import User, Customer, Company

class DateInput(forms.DateInput):
    input_type = 'date'

class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(
        widget=DateInput(),
        help_text='You must be at least 18 years old'
    )
    email = forms.EmailField(
        help_text='Enter a valid email address'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password','date_of_birth']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is required')
        
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, numbers, and underscores')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        
        # Basic email format validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Enter a valid email address')
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError('Password is required')
        
        # Password length
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        
        # Password complexity
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character')
        
        return password

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if not dob:
            raise ValidationError('Date of birth is required')
        
        # Calculate age
        today = timezone.now().date()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age < 18:
            raise ValidationError('You must be at least 18 years old to register')
        
        if age > 120:
            raise ValidationError('Please enter a valid date of birth')
        
        return dob

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation:
            if password != password_confirmation:
                raise ValidationError('Passwords do not match')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user

class CompanySignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    description = forms.CharField(
        widget=forms.Textarea,
        help_text='Provide a brief description of your company and services'
    )
    location = forms.CharField(
        max_length=255,
        help_text='Enter your company\'s primary location'
    )
    email = forms.EmailField(
        help_text='Enter your business email'
    )
    field = forms.ChoiceField(choices=(
        ('Air Conditioner', 'Air Conditioner'),
        ('All in One', 'All in One'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters')
    ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Company name is required')
        
        if len(username) < 3:
            raise ValidationError('Company name must be at least 3 characters long')
        
        if not re.match(r'^[a-zA-Z0-9\s_-]+$', username):
            raise ValidationError('Company name can only contain letters, numbers, spaces, hyphens, and underscores')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('This company name is already taken')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        
        # Basic email format validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Enter a valid business email address')
        
        # Common free email providers
        free_email_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
            'aol.com', 'mail.com', 'icloud.com'
        ]
        domain = email.split('@')[1].lower()
        if domain in free_email_providers:
            raise ValidationError('Please use a business email address, not a personal email service')
        
        return email

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError('Company description is required')
        
        if len(description) < 6:
            raise ValidationError('Description must be at least 6 characters long')
        
        if len(description) > 1000:
            raise ValidationError('Description must not exceed 1000 characters')
        
        return description

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location:
            raise ValidationError('Company location is required')
        
        if len(location) < 5:
            raise ValidationError('Please enter a more specific location')
        
        return location

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError('Password is required')
        
        # Password length
        if len(password) < 10:  # Stricter for companies
            raise ValidationError('Password must be at least 10 characters long')
        
        # Password complexity
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character')
        
        # Additional complexity for companies
        if len(re.findall(r'[0-9]', password)) < 2:
            raise ValidationError('Password must contain at least two numbers')
        if len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) < 2:
            raise ValidationError('Password must contain at least two special characters')
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation:
            if password != password_confirmation:
                raise ValidationError('Passwords do not match')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Company.objects.create(
                user=user,
                description=self.cleaned_data['description'],
                location=self.cleaned_data['location'],
                field=self.cleaned_data['field']
            )
        return user

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'

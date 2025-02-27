from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
import re

from .models import User, Customer, Company

class DateInput(forms.DateInput):
    input_type = 'date'

# register customer
class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(
        widget=DateInput(),
        help_text='You must be at least 18 years and above'
    )
    email = forms.EmailField(
        help_text='Enter a valid email address'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'date_of_birth']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is required')
        
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long')
        if re.search(r'\d', username):
            raise ValidationError("Username name should not contain numbers.")
        
        if not re.match(r'^[a-zA-Z_-]+$', username):
            raise ValidationError('Username can only contain letters, numbers, and underscores')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required')
        
        # Basic email format validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Enter a valid email address')

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')

        # List of free email providers (the ones you want to allow)
        allowed_email_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'mail.com', 'icloud.com'
        ]
        
        # Extract the domain part of the email (after '@')
        domain = email.split('@')[1].lower()

        # If the domain is NOT in the list of allowed providers, raise an error
        if domain not in allowed_email_providers:
            raise ValidationError("Invalid email address. Please use one of the allowed free email providers like Gmail, Yahoo, Hotmail, etc.")
        
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

    def clean_password_confirmation(self):
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
    
# register the compnay
class CompanySignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, required=True, 
        help_text="Enter your company name"
    )
    email = forms.EmailField(
        required=True, help_text="Enter your business email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, 
        help_text="Enter a strong password"
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput, required=True, 
        help_text="Confirm your password"
    )
    description = forms.CharField(
        widget=forms.Textarea, required=True, 
        help_text="Provide a brief description of your company and services"
    )
    location = forms.CharField(
        max_length=255, required=True, 
        help_text="Enter your company's primary location"
    )
    field_of_work = forms.ChoiceField(
        choices=(
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
        ),
        required=True
    )

    class Meta:
        model = Company
        fields = ['description', 'location', 'field_of_work']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check if the username is empty
        if not username:
            raise ValidationError('Username is required')

        # Check that the username does not contain digits (numbers)
        if re.search(r'\d', username):
            raise ValidationError("Company name should not contain numbers.")
        
        # Check if the username is only digits (should not be allowed)
        if username.isdigit():
            raise ValidationError("Company name should not contain only numbers.")
        
        # Check that the username contains only alphabetic characters, underscores, and hyphens (and is logically sensible)
        if not re.match(r'^[a-zA-Z_-]+$', username):
            raise ValidationError("Company name should only contain letters, underscores, and hyphens.")
        
        # Check if the username already exists in the User model
        if User.objects.filter(username=username).exists():
            raise ValidationError("This company name is already taken")
        
        return username

    def clean_description(self):
        description = self.cleaned_data.get('description')

        # Check that the description only contains alphabets, underscores, and parentheses
        if not re.match(r'^[A-Za-z_() ]*$', description):
            raise ValidationError("Description should only contain alphabets, underscores, or parentheses.")
        
        return description

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        
        free_email_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
            'aol.com', 'mail.com', 'icloud.com'
        ]
        domain = email.split('@')[1].lower()
        if domain in free_email_providers:
            raise ValidationError("Please use a business email address, personal email is not allowed")
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 10:
            raise ValidationError("Password must be at least 10 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character")
        return password

    def clean_password_confirmation(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        # print(password)
        # print(password_confirmation)
        # comparison_result = password != password_confirmation
        # print(f'Comparison result: {comparison_result}')
        if password and password_confirmation:
            if password != password_confirmation:
                raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
          #  is_company = True 
        )
        #user.is_company = True # Mark as company
      #  print(f"Before save: is_company = {user.is_company}") # Check before saving
        user.save()
      #  print(f"After save: is_company = {user.is_company}")  # Check after saving

        company = super().save(commit=False)
        company.user = user
        company.email = self.cleaned_data['email']

        if commit:
            company.save()

        return company


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

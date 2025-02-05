from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
# 
class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.user.username  # or you can return any other field

class Customer(models.Model):
    # Adding the user field as a OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Adding the name field
    name = models.CharField(max_length=100)  # New field for customer name
    
    # Adding the birth date field
    birth = models.DateField()

    def __str__(self):
        return self.user.username  # or you can return any other field
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(default='', unique=True, blank=False, null=False)
    description = models.TextField(default='', blank=False, null=False)
    location = models.CharField(default='', max_length=255, blank=False, null=False)
    field_of_work = models.CharField(
        max_length=70,
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
        blank=False, null=False
    )

    def __str__(self):
        return f"{self.user.username} - {self.email} - {self.field_of_work}"


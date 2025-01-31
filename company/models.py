from django.db import models

FIELD_CHOICES = [
    ('Air Conditioner', 'Air Conditioner'),
    ('All in One', 'All in One'),
    ('Carpentry', 'Carpentry'),
    ('Electricity', 'Electricity'),
    ('Gardening', 'Gardening'),
    ('Home Machines', 'Home Machines'),
    ('Housekeeping', 'Housekeeping'),
    ('Interior Design', 'Interior Design'),
    ('Locks', 'Locks'),
    ('Painting', 'Painting'),
    ('Plumbing', 'Plumbing'),
    ('Water Heaters', 'Water Heaters'),
]

class Company(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)  # Link company to a user
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    field_of_work = models.CharField(max_length=50, choices=FIELD_CHOICES)

    def __str__(self):
        return self.name

class Service(models.Model):
    company = models.ForeignKey(Company, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.contrib import admin
from .models import User, Customer, Company

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    #list_display = ("user", "field")
    list_display = ('user', 'email', 'field_of_work', 'location')  # Updated from 'field' to 'field_of_work'



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "birth")  # These fields must now exist in the Customer model

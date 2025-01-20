from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')  # Display these fields in the admin list view
    search_fields = ('user__username', 'phone_number')  # Allow searching by username or phone number

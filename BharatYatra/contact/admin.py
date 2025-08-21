from django.contrib import admin
from django.contrib.admin.sites import site
from contact.models import ContactData

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message' )
    search_fields = ('name', 'email', 'phone') 
admin.site.register(ContactData, ContactAdmin)


# Register your models here.

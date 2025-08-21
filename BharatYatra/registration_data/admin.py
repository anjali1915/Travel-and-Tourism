from django.contrib import admin
from django.contrib.admin.sites import site
from registration_data.models import CustomUser
class UserAdmin(admin.ModelAdmin):
    list_display = ('fullname','phone','email','username','password','gender')
    search_fields = ('email','phone')
admin.site.register(CustomUser,UserAdmin)
# Register your models here.

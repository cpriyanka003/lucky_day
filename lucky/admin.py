from django.contrib import admin
from django.contrib.auth import get_user_model
from lucky.models import *


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mobile_number', 'is_active', 'is_staff', 'country_code', 'first_name', 'last_name')
    search_fields = ('mobile_number',)


class UserMasterAdmin(admin.ModelAdmin):
	list_display = ['profile', 'mobile_number']


admin.site.site_header = 'Lucky-Day'
admin.site.register(UserMaster, UserMasterAdmin)
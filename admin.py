from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UInfo, Commodity

# Register your models here.

class UserInline(admin.StackedInline):
    model = UInfo
    can_delete = False
    verbose_name_plural = 'Extra info'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)

class CommodityAdmin(admin.ModelAdmin):
    list_filter = ['date']



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Commodity, CommodityAdmin)


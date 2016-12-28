from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UInfo, Commodity, Category, Tag

# Register your models here.

class UserInline(admin.StackedInline):
    model = UInfo
    can_delete = False
    verbose_name_plural = 'Extra info'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)

class CommodityAdmin(admin.ModelAdmin):
    list_filter = ['date']

class CategoryAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)


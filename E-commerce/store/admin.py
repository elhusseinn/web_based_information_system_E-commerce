from django.contrib import admin

from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from account.models import Account

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)

admin.site.register(Cart) 
admin.site.register(Order) 
admin.site.register(OrderItem) 
admin.site.register(Profile) 

admin.site.unregister(Group)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields=('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

from django.contrib import admin

from .models import UserAccount
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

from models import AuditEntry

class UserAccountInline(admin.StackedInline):
    model = UserAccount
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserAccountInline, )


# @admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'ip', 'action_date']
    list_filter = ['action',]
    search_fields = ('user',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(AuditEntry, AuditEntryAdmin)
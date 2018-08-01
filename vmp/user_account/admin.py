from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

from import_export import resources
from import_export.admin import ExportMixin
from import_export import fields

from models import AuditEntry, UserAccount


class UserResource(resources.ModelResource):
    related_uploads = fields.Field(column_name='upload_num')

    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined', 'last_login', )
        export_order = ('username', 'email', 'date_joined', 'last_login')

    def dehydrate_related_uploads(self, obj):
        return obj.useraccount.upload_set.count()


class UserAccountInline(admin.StackedInline):
    model = UserAccount
    can_delete = False


# Define a new User admin
class UserAdmin(ExportMixin, BaseUserAdmin):
    resource_class = UserResource
    inlines = (UserAccountInline, )
    list_display = ('username', 'email', 'date_joined', 'last_login', 'upload_count')

    def upload_count(self, model_instance):
        return model_instance.useraccount.upload_set.count()

# @admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'ip', 'action_date']
    list_filter = ['action', ]
    search_fields = ('user',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(AuditEntry, AuditEntryAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User , OtpCode
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form= UserChangeForm
    add_form= UserCreationForm
    list_display = ('phone_number', 'full_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        # (_('Personal Info'), {'fields': ('full_name', 'email')}),
        # (_('Permissions'), {'fields': ('is_admin', 'is_active', 'groups', 'user_permissions')}),
        # (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'full_name', 'email', 'password1', 'password2'),}),
    )
    search_fields = ('phone_number', 'full_name', 'email')
    ordering = ('full_name',)
    # filter_horizontal = ('groups', 'user_permissions')
    filter_horizontal = ()
    # empty_value_display = '-empty-'
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


# class OtpCodeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'phone_number', 'code', 'created']
#     search_fields = ['phone_number']
#     ordering = ['id']


# admin.site.register(OtpCode, OtpCodeAdmin)


# class AddressAdmin(admin.ModelAdmin):
#     list_display = ['id', 'get_address']
#     ordering = ['id']


# admin.site.register(Address, AddressAdmin)
# ************************************

# from django.contrib import admin

# from .models import User

# admin.site.register(User)
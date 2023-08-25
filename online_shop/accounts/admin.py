from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User , OtpCode
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'phone_number', 'is_admin')
	list_filter = ('is_admin',)
	readonly_fields = ('last_login',)

	fieldsets = (
		('Main', {'fields':('email', 'phone_number', 'full_name', 'password', 'address2', 'postal_code2')}),
		('Permissions', {'fields':('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
	)

	add_fieldsets = (
		(None, {'fields':('phone_number', 'email', 'full_name', 'password1', 'password2', 'address2', 'postal_code2')}),
	)

	search_fields = ('email', 'full_name')
	ordering = ('full_name',)
	filter_horizontal = ('groups', 'user_permissions')

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser
		if not is_superuser:
			form.base_fields['is_superuser'].disabled = True
		return form
    
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
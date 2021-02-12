from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserRegisterForm
from .models import User

# Register your models here.
class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	# form = UserUpdateForm
	add_form = UserRegisterForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display=('email', 'user_name', 'active',)
	list_filter = ('active','staff','admin','country','gender',)
	search_fields=['email','first_name','last_name']
	fieldsets = (
		('User', {'fields': ('email', 'phone', 'password')}),
		('Profile details', {'fields': ('first_name', 'last_name','gender','country',)}),
		('Permissions', {'fields': ('admin','staff','active',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
                'classes': ('wide',),
                'fields': ('email', 'phone', 'password',)
            }
		),
        ('Profile', {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name','gender','country',)
            }
		),
	)
	ordering = ('email',)
	filter_horizontal = ()


admin.site.register(User, UserAdmin)
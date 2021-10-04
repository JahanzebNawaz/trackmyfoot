from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Register your models here.

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'profile_image')
        }),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
        ('User Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'profile_image')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        })
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)

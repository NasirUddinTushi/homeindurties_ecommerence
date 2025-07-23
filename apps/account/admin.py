from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PasswordResetCode

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'is_used', 'created_at', 'reset_token')
    search_fields = ('email', 'code', 'reset_token')
    list_filter = ('is_used', 'created_at')

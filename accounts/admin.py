from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Profile, User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    filter_horizontal = ('favorite_tags',)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (('Display', {'fields': ('display_name',)}),)
    list_display = (
        'username',
        'email',
        'display_name',
        'is_staff',
        'is_active'
    )
    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    filter_horizontal = ('favorite_tags',)
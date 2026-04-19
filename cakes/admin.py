from django.contrib import admin

from .models import Cake, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'owner', 'price', 'created_at')
    list_filter = (
        'category',
        'tags',
        'created_at',
    )
    search_fields = (
        'name',
        'description'
    )

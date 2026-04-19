from django.contrib import admin

from .models import OrderLine, Order


# Register your models here.
class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'event_date',
        'created_at'
    )
    list_filter = (
        'status',
        'created_at'
    )
    search_fields = (
        'user__username',
        'note'
    )
    inlines = [OrderLineInline]
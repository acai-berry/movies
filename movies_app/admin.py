import django
from django.contrib import admin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html,  urlencode
from . import models

# Register your models here.

class PriceFilter(admin.SimpleListFilter):
        title = 'price'
        parameter_name = 'price'

        def lookups(self, request, model_admin):
            return [
                ('<10', 'Low'),
                ('>=10', 'High')
            ]

        def queryset(self, request, queryset):
            if self.value() == '<10':
                return queryset.filter(price__lt=10)
            elif self.value() == '>=10':
                return queryset.filter(price__gte=10)





@admin.register(models.Film)
class FilmAdmin(admin.ModelAdmin):
    autocomplete_fields = ['genre']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'price', 'genre', 'last_update']
    list_editable = ['price']
    list_per_page = 10
    list_filter = ['genre', 'last_update', PriceFilter]
    search_fields = ['title']
    



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:movies_app_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
    

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'films_count']
    search_fields = ['title']

    @admin.display(ordering='films_count')
    def films_count(self, genre):
        url = (reverse('admin:movies_app_film_changelist') 
        + '?'
        + urlencode({
            'genre__id': str(genre.id)
        }))
        return format_html('<a href="{}">{}</a>', url, genre.films_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(films_count=Count('film')) 


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['film']
    model = models.Order_Item
    min_num = 1
    max_num = 10
    extra = 0



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_per_page = 10


from django.contrib import admin

from .models import *

from django.contrib.auth.models import Group
from django.contrib.auth.models import User

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.site_header = 'Administración de Kenosis'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'document')
    search_fields = ('name', 'document')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'document')
    search_fields = ('name', 'document')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def sold_out(self, instance):
        return instance.is_sold_out

    sold_out.boolean = True
    sold_out.short_description = 'agotado'

    list_display = ('code', 'name', 'price', 'amount', 'sold_out',)
    search_fields = ('code', 'name',)


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    search_fields = ('id',)
    list_filter = ('date', 'register_type')
    list_display = ('id', 'date', 'register_type', 'value', 'description',)
    readonly_fields = ('client', 'description', 'register_type', 'product_name')
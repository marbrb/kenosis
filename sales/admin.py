from django.contrib import admin

from .models import *

from django.contrib.auth.models import Group
from django.contrib.auth.models import User

admin.site.site_header = 'Administración de Kenosis'

class BaseModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields

        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))

@admin.register(Client)
class ClientAdmin(BaseModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'document')
    search_fields = ('name', 'document')


@admin.register(Employee)
class EmployeeAdmin(BaseModelAdmin):
    list_display = ('name', 'phone_number', 'document')
    search_fields = ('name', 'document')


@admin.register(EstheticHouse)
class EstheticHouseAdmin(BaseModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    def sold_out(self, instance):
        return instance.is_sold_out

    sold_out.boolean = True
    sold_out.short_description = 'agotado'

    list_display = ('code', 'name', 'house', 'price', 'amount', 'sold_out',)
    search_fields = ('code', 'name',)
    list_filter = ('house',)


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    search_fields = ('id',)
    list_filter = ('date', 'register_type', 'owner')
    list_display = ('id', 'owner', 'date', 'register_type', 'value', 'description', 'product_name', 'is_pay_with_card')
    readonly_fields = ('client', 'description', 'register_type', 'product_name')

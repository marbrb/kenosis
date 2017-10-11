from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from .views import CreateSale
from .views import CreateExpense

urlpatterns = [
    url(
    	r'venta/', 
    	CreateSale.as_view(),
    	name='create_sale'
    ),

    url(
    	r'gasto/', 
    	CreateExpense.as_view(),
    	name='create_expense'
    ),

    url(
    	r'inicio/', 
    	TemplateView.as_view(template_name='sales/home'),
    	name='home'
    ),
]

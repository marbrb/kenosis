from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from .views import ProductSaleJSONView
from .views import ServiceSaleJSONView
from .views import CreateExpense
from .views import ProductDataJSONView
from .views import TodayRegistersListView

urlpatterns = [
    url(
        r'venta/producto', 
        ProductSaleJSONView.as_view(),
        name='create_product_sale'
    ),

    url(
    	r'venta/servicio', 
    	ServiceSaleJSONView.as_view(),
    	name='create_service_sale'
    ),

    url(
    	r'gasto/', 
    	CreateExpense.as_view(),
    	name='create_expense'
    ),

    url(
        r'^$',
        TemplateView.as_view(template_name='sales/home.html'),
        name='home'
    ), 

    url(
        r'producto/', 
        ProductDataJSONView.as_view(),
        name='producto'
    ),

    url(
    	r'registros/', 
    	TodayRegistersListView.as_view(),
    	name='registers'
    ),
    
    url(
        r'balance/',
        TemplateView.as_view(template_name='sales/lista.html'),
        name='balance'        
    ),
    
]

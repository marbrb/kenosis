from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from .views import CreateSale
from .views import CreateExpense
from .views import ProductDataJSONView
from .views import TodayRegistersListView

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
        name='home'        
    ),
    
]

from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import View

from .models import *
from .data import EXPENSE_TYPE
from .data import ENTRANCE_TYPE


class CreateSale(TemplateView):
	template_name = 'sales/create_sale.html'

	def post(self, *args, **kwargs):
		data = self.request.POST

		owner_document = data.get('owner_document')
		owner = Employee.objects.filter(document=owner_document).first()
		if not owner:
			return JsonResponse({
				'ok': False,
				'msg': 'No existe un empleado registado con esta cédula',
			})

		client_document = data.get('client_document')
		client = None
		if client_document:
			client = Client.objects.get(document=owner_document)

		description = data.get('description')
		value = data.get('value')

		# TODO: validar si llega bien el dato
		is_with_card = data.get('is_card')


		product_name = data.get('el_name')


		Register.objects.Create(
			owner=owner,
			client=client,
			description=description,
			value=value,
			register_type=ENTRANCE_TYPE,
			is_pay_with_card=is_with_card,
			product_name=product_name,
		)

		return JsonResponse({'ok': True})


class CreateExpense(TemplateView):
	template_name = 'sales/create_expense.html'

	def post(self, *args, **kwargs):
		data = self.request.POST

		owner_document = data.get('owner_document')
		owner = Employee.objects.filter(document=owner_document).first()
		if not owner:
			return JsonResponse({
				'ok': False,
				'msg': 'No existe un empleado registado con esta cédula',
			})

		description = data.get('description')
		value = data.get('value')

		Register.objects.Create(
			owner=owner,
			description=description,
			value=value,
			register_type=EXPENSE_TYPE,
		)


class ProductDataJSONView(View):
	def get(self, request, *args, **kwargs):
		product_id = request.GET.get('code')
		product = Product.objects.filter(id=product_id).first()
		if not product:
			return JsonResponse({
				'ok': False,
				'msg': 'Producto no encontrado',
			})

		return JsonResponse({
			'name': product.name,
			'price': product.price,
			'amount': product.amount,
		})

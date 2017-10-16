from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import View

from .models import *
from .data import EXPENSE_TYPE
from .data import ENTRANCE_TYPE


class CreateSale(TemplateView):
	template_name = 'sales/create_sale.html'

	def get_context_data(self, **kwargs):

		context = super(CreateSale, self).get_context_data(**kwargs)
		context['employees'] = Employee.objects.values('name')

		return context

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
			try:
				client = Client.objects.get(document=client_document)
			except:
				client = None

		description = data.get('description')
		value = int(data.get('value'))

		is_with_card = data.get('is_card')
		is_with_card = True if is_with_card == 'true' else False


		product_name = data.get('el_name')


		percent = int(data.get('percent'))
		admin_percent = 100 - percent

		employee_value = (value * percent) / 100
		admin_value = (value * admin_percent) / 100



		Register.objects.create(
			owner=owner,
			client=client,
			description=description,
			value=employee_value,
			register_type=ENTRANCE_TYPE,
			is_pay_with_card=is_with_card,
			product_name=product_name,
		)

		admin = Employee.objects.get(document='kenosis')

		Register.objects.create(
			owner=admin,
			client=client,
			description=description,
			value=admin_value,
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
		owner = Employee.objects.filter(document='kenosis').first()
		if not owner:
			return JsonResponse({
				'ok': False,
				'msg': 'El ususario kenosis no está registrado',
			})

		# TODO: ennviar usuario kenosis a un setting
		description = data.get('description')
		value = data.get('value')

		Register.objects.create(
			owner=owner,
			description=description,
			value=value,
			register_type=EXPENSE_TYPE,
		)

		return JsonResponse({'ok': True})


class ProductDataJSONView(View):
	def get(self, request, *args, **kwargs):
		product_id = request.GET.get('code')
		product = Product.objects.filter(code=product_id).first()
		if not product:
			return JsonResponse({
				'ok': False,
				'msg': 'Producto no encontrado',
			})

		return JsonResponse({
			'ok': True,
			'name': product.name,
			'price': product.price,
			'amount': product.amount,
		})

class TodayRegistersListView(View):
	def get(self, request, *args, **kwargs):
		yeison = {'data': []}

		# TODO: filtrar
		for reg in Register.objects.all():
			info = {
				'owner_name': reg.owner.name,
				'value': reg.value,
				'register_type': reg.get_register_type_display(),
				'is_with_card': reg.is_pay_with_card,
			}

			yeison['data'].append(info)

		return JsonResponse(yeison)
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.utils import timezone

from .models import *
from .data import EXPENSE_TYPE
from .data import ENTRANCE_TYPE


class ServiceSaleJSONView(TemplateView):
	template_name = 'sales/create_service_sale.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['employees'] = Employee.objects.all()

		return context

	def post(self, *args, **kwargs):
		data = self.request.POST

		is_with_card = data.get('is_card')
		is_with_card = True if is_with_card == 'true' else False

		owner_document = data.get('owner_document')
		owner = Employee.objects.filter(document=owner_document).first()

		client_document = data.get('client_document')
		client = None
		if client_document:
			try:
				client = Client.objects.get(document=client_document)
			except:
				client = None

		service_list = data.get('services')
		service_list = eval(service_list)

		for service in service_list:
			product_name = service['el_name']
			value = int(service['value'])
						
			percent = int(service['percent'])
			admin_percent = 100 - percent

			employee_value = (value * percent) / 100
			admin_value = (value * admin_percent) / 100

			Register.objects.create(
				owner=owner,
				client=client,
				value=employee_value,
				register_type=ENTRANCE_TYPE,
				is_pay_with_card=is_with_card,
				product_name=product_name,
			)

			admin = Employee.objects.get(document='kenosis')

			Register.objects.create(
				owner=admin,
				client=client,
				value=admin_value,
				register_type=ENTRANCE_TYPE,
				is_pay_with_card=is_with_card,
				product_name=product_name,
			)

		return JsonResponse({'ok': True})




class ProductSaleJSONView(TemplateView):
	template_name = 'sales/create_product_sale.html'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['employees'] = Employee.objects.all()

		return context

	def post(self, *args, **kwargs):
		data = self.request.POST

		owner_document = data.get('owner_document')
		owner = Employee.objects.filter(document=owner_document).first()

		client_document = data.get('client_document')
		client = None
		if client_document:
			try:
				client = Client.objects.get(document=client_document)
			except:
				client = None

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
			value=employee_value,
			register_type=ENTRANCE_TYPE,
			is_pay_with_card=is_with_card,
			product_name=product_name,
		)

		admin = Employee.objects.get(document='kenosis')

		Register.objects.create(
			owner=admin,
			client=client,
			value=admin_value,
			register_type=ENTRANCE_TYPE,
			is_pay_with_card=is_with_card,
			product_name=product_name,
		)

		product_code = data.get('product_code')
		product = Product.objects.get(code=int(product_code))
		product.amount -= 1
		product.save()

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
		if not str(product_id).isdigit():
			return JsonResponse({
				'ok': False,
				'msg': 'Producto no encontrado',
			})

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


		today = timezone.localtime(timezone.now())

		today_registers = Register.objects.filter(
			date__date=today.date()
		)

		today_cash = 0
		for register in today_registers.filter(
			is_pay_with_card=False,
			register_type=ENTRANCE_TYPE,
		):
			today_cash += register.value

		card_cash = 0
		for register in today_registers.filter(
			is_pay_with_card=True,
			register_type=ENTRANCE_TYPE,
		):
			card_cash += register.value


		# TODO: filtrar
		for reg in today_registers:
			info = {
				'owner_name': reg.owner.name,
				'value': reg.value,
				'register_type': reg.get_register_type_display(),
				'is_with_card': reg.is_pay_with_card,
			}

			yeison['data'].append(info)

				
				
		yeison['today_cash'] = today_cash
		yeison['card_cash'] = card_cash

		return JsonResponse(yeison)
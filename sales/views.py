from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.utils import timezone
from django.shortcuts import redirect

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

		if str(product_code).isdigit():
			product_code = int(product_code)
		else:
			product_code = str(product_code).strip()

		product = Product.objects.get(code=product_code)
		product.amount -= 1
		product.save()

		return JsonResponse({'ok': True})



class CreateExpense(TemplateView):
	template_name = 'sales/create_expense.html'

	def get(self, *args, **kwargs):
		max_date = timezone.now() - timezone.timedelta(days=30)
		Register.objects.filter(
			date__date__lt=max_date.date()
		).delete()

		return super().get(*args, **kwargs)

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
			product_id = product_id.strip()


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


class RegistersListView(View):
	def get(self, request, *args, **kwargs):
		date = timezone.localtime(timezone.now()).date()

		desired_date = kwargs.get('date')
		if desired_date:
			date = timezone.datetime.strptime(desired_date, "%d-%m-%Y").date()

		yeison = {'data': []}

		registers = Register.objects.filter(
			date__date=date
		)

		cash = 0
		for register in registers.filter(
			is_pay_with_card=False,
			register_type=ENTRANCE_TYPE,
		):
			cash += register.value

		card_cash = 0
		for register in registers.filter(
			is_pay_with_card=True,
			register_type=ENTRANCE_TYPE,
		):
			card_cash += register.value

		for reg in registers:
			info = {
				'owner_name': reg.owner.name,
				'value': reg.value,
				'register_type': reg.get_register_type_display(),
				'is_with_card': reg.is_pay_with_card,
			}

			yeison['data'].append(info)



		yeison['today_cash'] = cash
		yeison['card_cash'] = card_cash

		return JsonResponse(yeison)


class ReverseSaleJSONView(View):
	def get(self, request, *args, **kwargs):

		last_sale = Register.objects.filter(
			register_type=ENTRANCE_TYPE,
		).last()

		if not last_sale:
			return JsonResponse({
				'title': 'Eliminar Venta',
				'msg': 'No existen registros para eliminar',
				'type': 'red'
			})

		last_sale2 = Register.objects.get(
			id=last_sale.id - 1,
		).delete()

		last_sale.delete()

		return JsonResponse({
			'title': 'Eliminar Venta',
			'msg': 'La última venta fue eliminada',
			'type': 'green',
		})

class ReverseExpenseJSONView(View):
	def get(self, request, *args, **kwargs):

		last_expense = Register.objects.filter(
			register_type=EXPENSE_TYPE,
		).last()

		if not last_expense:
			return JsonResponse({
				'title': 'Eliminar Gasto',
				'msg': 'No existen registros para eliminar',
				'type': 'red',
			})

		last_expense.delete()

		return JsonResponse({
			'title': 'Eliminar Gasto',
			'msg': 'El último gasto fue eliminado',
			'type': 'green'
		})

class RegisterTemplateView(TemplateView):
	template_name = 'sales/lista.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['date'] = kwargs.get('date')

		return context

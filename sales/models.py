from django.db import models

from .data import REGISTER_TYPE_CHOICES
from .data import ENTRANCE_TYPE
from .data import EXPENSE_TYPE


class Client(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='nombre',
    )

    document = models.CharField(
        primary_key=True,
        max_length=30,
        verbose_name='cédula',
    )

    phone_number = models.CharField(
        max_length=10,
        verbose_name='celular'
    )

    email = models.CharField(
        max_length=255,
        verbose_name='correo electrónico',
        null=True,
    )

    birthday = models.DateField(
        verbose_name='Fecha de Cumpleaños',
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Product(models.Model):
    code = models.IntegerField(
        primary_key=True,
        verbose_name='código',
    )

    name = models.CharField(
        max_length=255,
        verbose_name='nombre',
        blank=True,
    )

    price = models.IntegerField(
        verbose_name='precio',
    )

    amount = models.IntegerField(
        verbose_name='cantidad',
    )

    @property
    def is_sold_out(self):
        return self.amount == 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Employee(models.Model):
    name = models.CharField(
        verbose_name='nombre',
        max_length=255,
    )

    document = models.CharField(
        primary_key=True,
        max_length=30,
        verbose_name='cédula',
    )

    phone_number = models.CharField(
        max_length=10,
        verbose_name='celular'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'


class Register(models.Model):
    owner = models.ForeignKey(
        'Employee',
        verbose_name='propietario'
    )

    client = models.ForeignKey(
        'Client',
        verbose_name='cliente',
        null=True,
    )

    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='descripción'
    )

    date = models.DateTimeField(
        auto_now=True,
        verbose_name='fecha',
    )

    value = models.IntegerField(
        verbose_name='valor',
    )

    register_type = models.PositiveSmallIntegerField(
        choices=REGISTER_TYPE_CHOICES,
        verbose_name='servicio',
    )

    @property
    def is_entrance(self):
        return self.register_type == ENTRANCE_TYPE
    @property
    def is_expense(self):
        return self.register_type == EXPENSE_TYPE

    def __str__(self):
        return 'Registro número {}'.format(
            self.id
        )

    class Meta:
        ordering = ['date',]
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

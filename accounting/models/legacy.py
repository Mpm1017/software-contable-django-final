"""
Modelos Legacy (compatibilidad con sistema anterior)
Estos modelos se mantienen para no perder datos existentes
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# Constantes para verbose_name
VERBOSE_NAME_DESCRIPCION = 'Descripción'


class Account(models.Model):
    """
    Modelo para las cuentas bancarias o de efectivo del usuario.
    Cada usuario puede tener múltiples cuentas.
    """
    ACCOUNT_TYPES = [
        ('BANK', 'Cuenta Bancaria'),
        ('CASH', 'Efectivo'),
        ('CREDIT', 'Tarjeta de Crédito'),
        ('SAVINGS', 'Cuenta de Ahorros'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='Usuario'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la Cuenta'
    )
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPES,
        default='BANK',
        verbose_name='Tipo de Cuenta'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Saldo'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=VERBOSE_NAME_DESCRIPCION
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )
    
    class Meta:
        verbose_name = 'Cuenta (Legacy)'
        verbose_name_plural = 'Cuentas (Legacy)'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.get_account_type_display()} (${self.balance})"


class Category(models.Model):
    """
    Modelo para las categorías de transacciones.
    Permite clasificar ingresos y gastos.
    """
    CATEGORY_TYPES = [
        ('INCOME', 'Ingreso'),
        ('EXPENSE', 'Gasto'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Usuario'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la Categoría'
    )
    category_type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES,
        verbose_name='Tipo de Categoría'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=VERBOSE_NAME_DESCRIPCION
    )
    color = models.CharField(
        max_length=7,
        default='#667eea',
        verbose_name='Color',
        help_text='Color en formato hexadecimal (ej: #667eea)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )
    
    class Meta:
        verbose_name = 'Categoría (Legacy)'
        verbose_name_plural = 'Categorías (Legacy)'
        ordering = ['category_type', 'name']
        unique_together = ['user', 'name', 'category_type']
        
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class Transaction(models.Model):
    """
    Modelo para las transacciones financieras.
    Registra todos los movimientos de dinero (ingresos y gastos).
    """
    TRANSACTION_TYPES = [
        ('INCOME', 'Ingreso'),
        ('EXPENSE', 'Gasto'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Usuario'
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Cuenta'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Categoría'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        verbose_name='Tipo de Transacción'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Monto'
    )
    description = models.CharField(
        max_length=255,
        verbose_name=VERBOSE_NAME_DESCRIPCION
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas Adicionales'
    )
    transaction_date = models.DateField(
        verbose_name='Fecha de Transacción'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    class Meta:
        verbose_name = 'Transacción (Legacy)'
        verbose_name_plural = 'Transacciones (Legacy)'
        ordering = ['-transaction_date', '-created_at']
        
    def __str__(self):
        return f"{self.get_transaction_type_display()} - ${self.amount} - {self.description}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribimos el método save para actualizar el saldo de la cuenta
        automáticamente cuando se crea o modifica una transacción.
        """
        # Verificamos si es una nueva transacción o una actualización
        is_new = self.pk is None
        
        if not is_new:
            # Si es una actualización, primero revertimos el efecto de la transacción anterior
            old_transaction = Transaction.objects.get(pk=self.pk)
            if old_transaction.transaction_type == 'INCOME':
                old_transaction.account.balance -= old_transaction.amount
            else:
                old_transaction.account.balance += old_transaction.amount
            old_transaction.account.save()
        
        # Guardamos la transacción
        super().save(*args, **kwargs)
        
        # Actualizamos el saldo de la cuenta
        if self.transaction_type == 'INCOME':
            self.account.balance += self.amount
        else:
            self.account.balance -= self.amount
        self.account.save()
    
    def delete(self, *args, **kwargs):
        """
        Sobrescribimos el método delete para revertir el efecto en el saldo
        cuando se elimina una transacción.
        """
        # Revertimos el efecto en el saldo
        if self.transaction_type == 'INCOME':
            self.account.balance -= self.amount
        else:
            self.account.balance += self.amount
        self.account.save()
        
        # Eliminamos la transacción
        super().delete(*args, **kwargs)

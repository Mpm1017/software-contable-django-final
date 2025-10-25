"""
Clase Base Abstracta para el Plan de Cuentas
Aplica: Herencia, Polimorfismo, Encapsulamiento, Abstracción
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from abc import ABC, abstractmethod


class CuentaContable(models.Model):
    """
    Clase base abstracta para todas las cuentas contables.
    
    Conceptos POO aplicados:
    - ABSTRACCIÓN: Define la interfaz común para todas las cuentas
    - ENCAPSULAMIENTO: Métodos privados y públicos bien definidos
    - HERENCIA: Base para Activo, Pasivo, Patrimonio, Ingreso, Gasto
    """
    
    # Tipos de cuenta (para la jerarquía)
    TIPO_CUENTA_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('PASIVO', 'Pasivo'),
        ('PATRIMONIO', 'Patrimonio'),
        ('INGRESO', 'Ingreso'),
        ('GASTO', 'Gasto'),
    ]
    
    # Naturaleza de la cuenta (Deudora o Acreedora)
    NATURALEZA_CHOICES = [
        ('DEUDORA', 'Deudora'),
        ('ACREEDORA', 'Acreedora'),
    ]
    
    # Atributos básicos
    codigo = models.CharField(
        max_length=20,
        unique=True,
        help_text='Código único de la cuenta (ej: 1.1.01)'
    )
    nombre = models.CharField(
        max_length=200,
        help_text='Nombre de la cuenta'
    )
    descripcion = models.TextField(
        blank=True,
        help_text='Descripción detallada de la cuenta'
    )
    
    # Jerarquía (auto-referencia para estructura de árbol)
    cuenta_padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='subcuentas',
        help_text='Cuenta padre en la jerarquía'
    )
    
    # Nivel en la jerarquía (1 = raíz, 2 = subcuenta, etc.)
    nivel = models.IntegerField(
        default=1,
        help_text='Nivel en la jerarquía del plan de cuentas'
    )
    
    # Tipo y naturaleza
    tipo_cuenta = models.CharField(
        max_length=20,
        choices=TIPO_CUENTA_CHOICES,
        help_text='Tipo de cuenta según clasificación contable'
    )
    naturaleza = models.CharField(
        max_length=10,
        choices=NATURALEZA_CHOICES,
        help_text='Naturaleza de la cuenta (Deudora o Acreedora)'
    )
    
    # Saldo actual (encapsulado)
    _saldo = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        db_column='saldo',
        help_text='Saldo actual de la cuenta'
    )
    
    # Control
    es_cuenta_detalle = models.BooleanField(
        default=True,
        help_text='Si es True, permite movimientos. Si es False, solo agrupa subcuentas'
    )
    activa = models.BooleanField(
        default=True,
        help_text='Indica si la cuenta está activa'
    )
    
    # Usuario y auditoría
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='cuentas_contables'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = False  # NO es abstracta, crea tabla en BD para polimorfismo
        ordering = ['codigo']
        verbose_name = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    # ENCAPSULAMIENTO: Property para acceder al saldo
    @property
    def saldo(self):
        """Obtiene el saldo actual de la cuenta"""
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        """Establece el saldo (con validación)"""
        if valor < 0 and not self._permite_saldo_negativo():
            raise ValidationError(f"La cuenta {self.nombre} no permite saldo negativo")
        self._saldo = valor
    
    # ABSTRACCIÓN: Métodos que deben implementar las subclases
    def registrar_movimiento(self, monto, tipo_movimiento):
        """
        Registra un movimiento en la cuenta.
        
        Args:
            monto (Decimal): Monto del movimiento
            tipo_movimiento (str): 'DEBITO' o 'CREDITO'
        
        POLIMORFISMO: Cada tipo de cuenta implementa este método de forma diferente
        """
        raise NotImplementedError("Las subclases deben implementar registrar_movimiento()")
    
    def calcular_saldo(self):
        """
        Calcula el saldo de la cuenta basado en sus movimientos.
        
        Returns:
            Decimal: Saldo calculado
        
        POLIMORFISMO: Cada tipo de cuenta calcula su saldo de forma diferente
        """
        raise NotImplementedError("Las subclases deben implementar calcular_saldo()")
    
    # ENCAPSULAMIENTO: Métodos privados (helper methods)
    def _permite_saldo_negativo(self):
        """Determina si la cuenta permite saldo negativo"""
        # Por defecto, solo las cuentas de Pasivo y Patrimonio pueden tener saldo negativo
        return self.tipo_cuenta in ['PASIVO', 'PATRIMONIO']
    
    def _validar_movimiento(self, monto, tipo_movimiento):
        """Valida que el movimiento sea correcto"""
        if monto <= 0:
            raise ValidationError("El monto debe ser mayor a cero")
        
        if tipo_movimiento not in ['DEBITO', 'CREDITO']:
            raise ValidationError("El tipo de movimiento debe ser DEBITO o CREDITO")
        
        if not self.es_cuenta_detalle:
            raise ValidationError(
                f"La cuenta {self.nombre} es de agrupación y no permite movimientos directos"
            )
        
        if not self.activa:
            raise ValidationError(f"La cuenta {self.nombre} está inactiva")
    
    # ENCAPSULAMIENTO: Métodos públicos
    def obtener_jerarquia_completa(self):
        """
        Retorna la ruta completa de la cuenta en la jerarquía.
        
        Returns:
            str: Ruta completa (ej: "Activo > Activo Corriente > Efectivo")
        """
        if self.cuenta_padre:
            return f"{self.cuenta_padre.obtener_jerarquia_completa()} > {self.nombre}"
        return self.nombre
    
    def obtener_subcuentas(self, recursivo=False):
        """
        Obtiene las subcuentas de esta cuenta.
        
        Args:
            recursivo (bool): Si es True, obtiene todas las subcuentas recursivamente
        
        Returns:
            QuerySet: Subcuentas
        """
        if not recursivo:
            return self.subcuentas.all()
        
        # Recursivo: obtener todas las subcuentas en todos los niveles
        subcuentas = list(self.subcuentas.all())
        for subcuenta in list(subcuentas):
            subcuentas.extend(subcuenta.obtener_subcuentas(recursivo=True))
        return subcuentas
    
    def tiene_movimientos(self):
        """Verifica si la cuenta tiene movimientos registrados"""
        return self.movimientos.exists()
    
    def puede_eliminarse(self):
        """Verifica si la cuenta puede ser eliminada"""
        return not self.tiene_movimientos() and not self.subcuentas.exists()
    
    def clean(self):
        """Validaciones del modelo"""
        super().clean()
        
        # Validar que el código sea único
        if CuentaContable.objects.filter(codigo=self.codigo).exclude(pk=self.pk).exists():
            raise ValidationError({'codigo': 'Ya existe una cuenta con este código'})
        
        # Validar nivel jerárquico
        if self.cuenta_padre:
            self.nivel = self.cuenta_padre.nivel + 1
        else:
            self.nivel = 1
        
        # Validar que la cuenta padre sea del mismo tipo
        if self.cuenta_padre and self.cuenta_padre.tipo_cuenta != self.tipo_cuenta:
            raise ValidationError(
                'La cuenta padre debe ser del mismo tipo que la cuenta hija'
            )
    
    def save(self, *args, **kwargs):
        """Override de save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)

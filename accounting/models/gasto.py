"""
Modelos para Cuentas de Gasto
Aplica: Herencia, Polimorfismo
"""
from django.db import models
from decimal import Decimal
from .cuenta_base import CuentaContable


class Gasto(CuentaContable):
    """
    Clase para cuentas de Gasto.
    
    HERENCIA: Hereda de CuentaContable
    POLIMORFISMO: Implementa registrar_movimiento() de forma específica
    
    Naturaleza: DEUDORA
    - Aumenta con DÉBITO
    - Disminuye con CRÉDITO
    
    Ejemplos:
    - Costo de ventas
    - Gastos administrativos
    - Gastos de ventas
    - Gastos financieros
    """
    
    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        proxy = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.pk:
            self.tipo_cuenta = 'GASTO'
            self.naturaleza = 'DEUDORA'
    
    def registrar_movimiento(self, monto, tipo_movimiento):
        """
        POLIMORFISMO: Implementación específica para Gasto
        
        Gasto (Naturaleza Deudora):
        - DÉBITO: Aumenta el saldo
        - CRÉDITO: Disminuye el saldo (reversiones, ajustes)
        """
        self._validar_movimiento(monto, tipo_movimiento)
        
        monto = Decimal(str(monto))
        
        if tipo_movimiento == 'DEBITO':
            self._saldo += monto
        elif tipo_movimiento == 'CREDITO':
            self._saldo -= monto
        
        self.save()
    
    def calcular_saldo(self):
        """
        POLIMORFISMO: Calcula el saldo del Gasto
        
        Saldo = Suma de Débitos - Suma de Créditos
        """
        from .asiento_contable import Movimiento
        
        debitos = Movimiento.objects.filter(
            cuenta=self,
            asiento__estado='REGISTRADO'
        ).aggregate(total=models.Sum('debito'))['total'] or Decimal('0')
        
        creditos = Movimiento.objects.filter(
            cuenta=self,
            asiento__estado='REGISTRADO'
        ).aggregate(total=models.Sum('credito'))['total'] or Decimal('0')
        
        return debitos - creditos
    
    def save(self, *args, **kwargs):
        if not self.codigo.startswith('5'):
            raise ValueError("Las cuentas de Gasto deben tener código 5.x")
        super().save(*args, **kwargs)

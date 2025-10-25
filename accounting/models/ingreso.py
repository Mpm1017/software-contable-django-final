"""
Modelos para Cuentas de Ingreso
Aplica: Herencia, Polimorfismo
"""
from django.db import models
from decimal import Decimal
from .cuenta_base import CuentaContable


class Ingreso(CuentaContable):
    """
    Clase para cuentas de Ingreso.
    
    HERENCIA: Hereda de CuentaContable
    POLIMORFISMO: Implementa registrar_movimiento() de forma específica
    
    Naturaleza: ACREEDORA
    - Aumenta con CRÉDITO
    - Disminuye con DÉBITO
    
    Ejemplos:
    - Ventas
    - Ingresos por servicios
    - Ingresos financieros
    """
    
    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        proxy = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.pk:
            self.tipo_cuenta = 'INGRESO'
            self.naturaleza = 'ACREEDORA'
    
    def registrar_movimiento(self, monto, tipo_movimiento):
        """
        POLIMORFISMO: Implementación específica para Ingreso
        
        Ingreso (Naturaleza Acreedora):
        - CRÉDITO: Aumenta el saldo
        - DÉBITO: Disminuye el saldo (devoluciones, descuentos)
        """
        self._validar_movimiento(monto, tipo_movimiento)
        
        monto = Decimal(str(monto))
        
        if tipo_movimiento == 'CREDITO':
            self._saldo += monto
        elif tipo_movimiento == 'DEBITO':
            self._saldo -= monto
        
        self.save()
    
    def calcular_saldo(self):
        """
        POLIMORFISMO: Calcula el saldo del Ingreso
        
        Saldo = Suma de Créditos - Suma de Débitos
        """
        from .asiento_contable import Movimiento
        
        creditos = Movimiento.objects.filter(
            cuenta=self,
            asiento__estado='REGISTRADO'
        ).aggregate(total=models.Sum('credito'))['total'] or Decimal('0')
        
        debitos = Movimiento.objects.filter(
            cuenta=self,
            asiento__estado='REGISTRADO'
        ).aggregate(total=models.Sum('debito'))['total'] or Decimal('0')
        
        return creditos - debitos
    
    def save(self, *args, **kwargs):
        if not self.codigo.startswith('4'):
            raise ValueError("Las cuentas de Ingreso deben tener código 4.x")
        super().save(*args, **kwargs)

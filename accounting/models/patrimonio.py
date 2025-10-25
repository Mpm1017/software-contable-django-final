"""
Modelos para Cuentas de Patrimonio
Aplica: Herencia, Polimorfismo
"""
from django.db import models
from decimal import Decimal
from .cuenta_base import CuentaContable


class Patrimonio(CuentaContable):
    """
    Clase para cuentas de Patrimonio.
    
    HERENCIA: Hereda de CuentaContable
    POLIMORFISMO: Implementa registrar_movimiento() de forma específica
    
    Naturaleza: ACREEDORA
    - Aumenta con CRÉDITO
    - Disminuye con DÉBITO
    
    Ejemplos:
    - Capital social
    - Utilidades retenidas
    - Reservas
    """
    
    class Meta:
        verbose_name = 'Patrimonio'
        verbose_name_plural = 'Patrimonio'
        proxy = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.pk:
            self.tipo_cuenta = 'PATRIMONIO'
            self.naturaleza = 'ACREEDORA'
    
    def registrar_movimiento(self, monto, tipo_movimiento):
        """
        POLIMORFISMO: Implementación específica para Patrimonio
        
        Patrimonio (Naturaleza Acreedora):
        - CRÉDITO: Aumenta el saldo
        - DÉBITO: Disminuye el saldo
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
        POLIMORFISMO: Calcula el saldo del Patrimonio
        
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
        if not self.codigo.startswith('3'):
            raise ValueError("Las cuentas de Patrimonio deben tener código 3.x")
        super().save(*args, **kwargs)

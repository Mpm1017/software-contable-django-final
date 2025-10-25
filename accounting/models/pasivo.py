"""
Modelos para Cuentas de Pasivo
Aplica: Herencia, Polimorfismo
"""
from django.db import models
from decimal import Decimal
from .cuenta_base import CuentaContable


class Pasivo(CuentaContable):
    """
    Clase para cuentas de Pasivo.
    
    HERENCIA: Hereda de CuentaContable
    POLIMORFISMO: Implementa registrar_movimiento() de forma específica
    
    Naturaleza: ACREEDORA
    - Aumenta con CRÉDITO
    - Disminuye con DÉBITO
    """
    
    class Meta:
        verbose_name = 'Pasivo'
        verbose_name_plural = 'Pasivos'
        proxy = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.pk:
            self.tipo_cuenta = 'PASIVO'
            self.naturaleza = 'ACREEDORA'
    
    def registrar_movimiento(self, monto, tipo_movimiento):
        """
        POLIMORFISMO: Implementación específica para Pasivo
        
        Pasivo (Naturaleza Acreedora):
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
        POLIMORFISMO: Calcula el saldo del Pasivo
        
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


class PasivoCorriente(Pasivo):
    """
    Pasivos Corrientes (Corto Plazo)
    
    HERENCIA: Hereda de Pasivo
    
    Ejemplos:
    - Cuentas por pagar
    - Deuda a corto plazo
    - Provisiones
    """
    
    class Meta:
        verbose_name = 'Pasivo Corriente'
        verbose_name_plural = 'Pasivos Corrientes'
        proxy = True
    
    def save(self, *args, **kwargs):
        if not self.codigo.startswith('2.1'):
            raise ValueError("Los Pasivos Corrientes deben tener código 2.1.x")
        super().save(*args, **kwargs)


class PasivoNoCorriente(Pasivo):
    """
    Pasivos No Corrientes (Largo Plazo)
    
    HERENCIA: Hereda de Pasivo
    
    Ejemplos:
    - Deuda a largo plazo
    - Obligaciones financieras
    """
    
    class Meta:
        verbose_name = 'Pasivo No Corriente'
        verbose_name_plural = 'Pasivos No Corrientes'
        proxy = True
    
    def save(self, *args, **kwargs):
        if not self.codigo.startswith('2.2'):
            raise ValueError("Los Pasivos No Corrientes deben tener código 2.2.x")
        super().save(*args, **kwargs)

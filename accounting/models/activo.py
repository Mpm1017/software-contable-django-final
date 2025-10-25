"""
Modelos para Cuentas de Activo
Aplica: Herencia, Polimorfismo
"""
from django.db import models
from decimal import Decimal
from .cuenta_base import CuentaContable


class Activo(CuentaContable):
    """
    Clase para cuentas de Activo.
    
    HERENCIA: Hereda de CuentaContable
    POLIMORFISMO: Implementa registrar_movimiento() de forma específica
    
    Naturaleza: DEUDORA
    - Aumenta con DÉBITO
    - Disminuye con CRÉDITO
    """
    
    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
        proxy = False  # No es proxy, crea su propia tabla
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer valores por defecto para Activo
        if not self.pk:  # Solo para nuevas instancias
            self.tipo_cuenta = 'ACTIVO'
            self.naturaleza = 'DEUDORA'
    
    def registrar_movimiento(self, monto, tipo_movimiento):
        """
        POLIMORFISMO: Implementación específica para Activo
        
        Activo (Naturaleza Deudora):
        - DÉBITO: Aumenta el saldo
        - CRÉDITO: Disminuye el saldo
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
        POLIMORFISMO: Calcula el saldo del Activo
        
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


class ActivoCorriente(Activo):
    """
    Activos Corrientes (Circulantes)
    
    HERENCIA: Hereda de Activo
    
    Ejemplos:
    - Efectivo y equivalentes
    - Cuentas por cobrar
    - Inventarios
    - Gastos pagados por anticipado
    """
    
    class Meta:
        verbose_name = 'Activo Corriente'
        verbose_name_plural = 'Activos Corrientes'
        proxy = True  # Usa la misma tabla que Activo
    
    def save(self, *args, **kwargs):
        # Asegurar que el código comience con 1.1
        if not self.codigo.startswith('1.1'):
            raise ValueError("Los Activos Corrientes deben tener código 1.1.x")
        super().save(*args, **kwargs)


class ActivoNoCorriente(Activo):
    """
    Activos No Corrientes (Fijos)
    
    HERENCIA: Hereda de Activo
    
    Ejemplos:
    - Propiedad, planta y equipo
    - Activos intangibles
    - Inversiones a largo plazo
    """
    
    class Meta:
        verbose_name = 'Activo No Corriente'
        verbose_name_plural = 'Activos No Corrientes'
        proxy = True
    
    def save(self, *args, **kwargs):
        # Asegurar que el código comience con 1.2
        if not self.codigo.startswith('1.2'):
            raise ValueError("Los Activos No Corrientes deben tener código 1.2.x")
        super().save(*args, **kwargs)

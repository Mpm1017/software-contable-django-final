"""
Modelos para Asientos Contables y Movimientos
Aplica: Composición, Encapsulamiento
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db.models import Sum


class AsientoContable(models.Model):
    """
    Asiento Contable - Registro de transacciones según partida doble.
    
    COMPOSICIÓN: Un asiento está COMPUESTO por múltiples Movimientos
    ENCAPSULAMIENTO: Lógica de validación y registro encapsulada
    
    Principio de Partida Doble: Débitos = Créditos
    """
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('REGISTRADO', 'Registrado'),
        ('ANULADO', 'Anulado'),
    ]
    
    # Identificación
    numero = models.CharField(
        max_length=20,
        unique=True,
        help_text='Número único del asiento (ej: AS-2025-001)'
    )
    fecha = models.DateField(
        help_text='Fecha del asiento contable'
    )
    
    # Descripción
    descripcion = models.TextField(
        help_text='Descripción detallada del asiento'
    )
    referencia = models.CharField(
        max_length=100,
        blank=True,
        help_text='Referencia externa (número de factura, recibo, etc.)'
    )
    
    # Estado y control
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='BORRADOR',
        help_text='Estado actual del asiento'
    )
    
    # Usuario y auditoría
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='asientos_contables',
        help_text='Usuario que creó el asiento'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fecha_registro = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha y hora en que se registró el asiento'
    )
    fecha_anulacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha y hora en que se anuló el asiento'
    )
    
    class Meta:
        ordering = ['-fecha', '-numero']
        verbose_name = 'Asiento Contable'
        verbose_name_plural = 'Asientos Contables'
        indexes = [
            models.Index(fields=['fecha', 'estado']),
            models.Index(fields=['numero']),
        ]
    
    def __str__(self):
        return f"{self.numero} - {self.fecha} - {self.descripcion[:50]}"
    
    # ENCAPSULAMIENTO: Métodos públicos
    
    def esta_balanceado(self):
        """
        Verifica si el asiento está balanceado (Débitos = Créditos).
        
        Returns:
            bool: True si está balanceado, False en caso contrario
        """
        totales = self.movimientos.aggregate(
            total_debitos=Sum('debito'),
            total_creditos=Sum('credito')
        )
        
        total_debitos = totales['total_debitos'] or Decimal('0.00')
        total_creditos = totales['total_creditos'] or Decimal('0.00')
        
        # Comparar con tolerancia de 2 decimales
        return abs(total_debitos - total_creditos) < Decimal('0.01')
    
    def obtener_total_debitos(self):
        """Obtiene el total de débitos del asiento"""
        total = self.movimientos.aggregate(total=Sum('debito'))['total']
        return total or Decimal('0.00')
    
    def obtener_total_creditos(self):
        """Obtiene el total de créditos del asiento"""
        total = self.movimientos.aggregate(total=Sum('credito'))['total']
        return total or Decimal('0.00')
    
    def obtener_diferencia(self):
        """Obtiene la diferencia entre débitos y créditos"""
        return self.obtener_total_debitos() - self.obtener_total_creditos()
    
    def puede_registrarse(self):
        """
        Verifica si el asiento puede ser registrado.
        
        Returns:
            tuple: (bool, str) - (puede_registrarse, mensaje_error)
        """
        if self.estado != 'BORRADOR':
            return False, "Solo se pueden registrar asientos en estado BORRADOR"
        
        if not self.movimientos.exists():
            return False, "El asiento debe tener al menos un movimiento"
        
        if self.movimientos.count() < 2:
            return False, "El asiento debe tener al menos 2 movimientos (débito y crédito)"
        
        if not self.esta_balanceado():
            diferencia = self.obtener_diferencia()
            return False, f"El asiento no está balanceado. Diferencia: ${diferencia}"
        
        return True, "OK"
    
    def registrar(self):
        """
        Registra el asiento contable, aplicando los movimientos a las cuentas.
        
        ENCAPSULAMIENTO: Proceso completo de registro encapsulado
        """
        from django.utils import timezone
        
        # Validar que puede registrarse
        puede, mensaje = self.puede_registrarse()
        if not puede:
            raise ValidationError(mensaje)
        
        # Aplicar cada movimiento a su cuenta
        for movimiento in self.movimientos.all():
            movimiento.aplicar()
        
        # Cambiar estado
        self.estado = 'REGISTRADO'
        self.fecha_registro = timezone.now()
        self.save()
    
    def puede_anularse(self):
        """Verifica si el asiento puede ser anulado"""
        if self.estado != 'REGISTRADO':
            return False, "Solo se pueden anular asientos REGISTRADOS"
        return True, "OK"
    
    def anular(self, motivo=""):
        """
        Anula el asiento contable, revirtiendo los movimientos.
        
        Args:
            motivo (str): Motivo de la anulación
        """
        from django.utils import timezone
        
        puede, mensaje = self.puede_anularse()
        if not puede:
            raise ValidationError(mensaje)
        
        # Revertir cada movimiento
        for movimiento in self.movimientos.all():
            movimiento.revertir()
        
        # Cambiar estado
        self.estado = 'ANULADO'
        self.fecha_anulacion = timezone.now()
        if motivo:
            self.descripcion += f"\n\nANULADO: {motivo}"
        self.save()
    
    def duplicar(self):
        """
        Crea una copia del asiento en estado BORRADOR.
        
        Returns:
            AsientoContable: Nuevo asiento duplicado
        """
        # Crear nuevo asiento
        nuevo_asiento = AsientoContable.objects.create(
            numero=f"{self.numero}-COPIA",
            fecha=self.fecha,
            descripcion=f"COPIA DE: {self.descripcion}",
            referencia=self.referencia,
            usuario=self.usuario,
            estado='BORRADOR'
        )
        
        # Copiar movimientos
        for movimiento in self.movimientos.all():
            Movimiento.objects.create(
                asiento=nuevo_asiento,
                cuenta=movimiento.cuenta,
                debito=movimiento.debito,
                credito=movimiento.credito,
                descripcion=movimiento.descripcion
            )
        
        return nuevo_asiento
    
    def clean(self):
        """Validaciones del modelo"""
        super().clean()
        
        # Validar número único
        if AsientoContable.objects.filter(numero=self.numero).exclude(pk=self.pk).exists():
            raise ValidationError({'numero': 'Ya existe un asiento con este número'})
    
    def save(self, *args, **kwargs):
        """Override de save"""
        self.full_clean()
        super().save(*args, **kwargs)


class Movimiento(models.Model):
    """
    Movimiento contable - Parte de un asiento contable.
    
    COMPOSICIÓN: Un Movimiento es parte de un AsientoContable
    
    Cada movimiento representa un débito o un crédito en una cuenta.
    """
    
    # Relación con asiento (COMPOSICIÓN)
    asiento = models.ForeignKey(
        AsientoContable,
        on_delete=models.CASCADE,  # Si se elimina el asiento, se eliminan los movimientos
        related_name='movimientos',
        help_text='Asiento contable al que pertenece este movimiento'
    )
    
    # Relación con cuenta
    cuenta = models.ForeignKey(
        'CuentaContable',
        on_delete=models.PROTECT,  # No se puede eliminar una cuenta con movimientos
        related_name='movimientos',
        help_text='Cuenta contable afectada'
    )
    
    # Montos (solo uno debe tener valor, el otro debe ser 0)
    debito = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Monto del débito'
    )
    credito = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Monto del crédito'
    )
    
    # Descripción específica del movimiento
    descripcion = models.CharField(
        max_length=200,
        blank=True,
        help_text='Descripción específica de este movimiento'
    )
    
    # Control
    aplicado = models.BooleanField(
        default=False,
        help_text='Indica si el movimiento ya fue aplicado a la cuenta'
    )
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
    
    def __str__(self):
        if self.debito > 0:
            return f"Débito: {self.cuenta.nombre} - ${self.debito}"
        else:
            return f"Crédito: {self.cuenta.nombre} - ${self.credito}"
    
    def obtener_monto(self):
        """Retorna el monto del movimiento (débito o crédito)"""
        return self.debito if self.debito > 0 else self.credito
    
    def obtener_tipo(self):
        """Retorna el tipo de movimiento"""
        return 'DEBITO' if self.debito > 0 else 'CREDITO'
    
    def aplicar(self):
        """
        Aplica el movimiento a la cuenta correspondiente.
        
        ENCAPSULAMIENTO: Lógica de aplicación encapsulada
        """
        if self.aplicado:
            raise ValidationError("Este movimiento ya fue aplicado")
        
        if self.asiento.estado != 'REGISTRADO':
            raise ValidationError("Solo se pueden aplicar movimientos de asientos REGISTRADOS")
        
        # Aplicar a la cuenta usando polimorfismo
        if self.debito > 0:
            self.cuenta.registrar_movimiento(self.debito, 'DEBITO')
        elif self.credito > 0:
            self.cuenta.registrar_movimiento(self.credito, 'CREDITO')
        
        self.aplicado = True
        self.save()
    
    def revertir(self):
        """
        Revierte el movimiento de la cuenta.
        
        ENCAPSULAMIENTO: Lógica de reversión encapsulada
        """
        if not self.aplicado:
            raise ValidationError("Este movimiento no ha sido aplicado")
        
        # Revertir usando el tipo opuesto
        if self.debito > 0:
            self.cuenta.registrar_movimiento(self.debito, 'CREDITO')
        elif self.credito > 0:
            self.cuenta.registrar_movimiento(self.credito, 'DEBITO')
        
        self.aplicado = False
        self.save()
    
    def clean(self):
        """Validaciones del modelo"""
        super().clean()
        
        # Validar que solo uno tenga valor
        if self.debito > 0 and self.credito > 0:
            raise ValidationError(
                "Un movimiento no puede tener débito y crédito simultáneamente"
            )
        
        if self.debito == 0 and self.credito == 0:
            raise ValidationError(
                "Un movimiento debe tener débito o crédito"
            )
        
        # Validar que la cuenta permita movimientos
        if self.cuenta and not self.cuenta.es_cuenta_detalle:
            raise ValidationError(
                f"La cuenta {self.cuenta.nombre} es de agrupación y no permite movimientos"
            )
    
    def save(self, *args, **kwargs):
        """Override de save"""
        self.full_clean()
        super().save(*args, **kwargs)

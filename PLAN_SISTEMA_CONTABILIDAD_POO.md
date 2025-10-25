# 📊 Plan de Implementación: Sistema de Contabilidad con POO

## 🎯 Objetivo
Transformar el sistema actual en un Sistema de Contabilidad completo aplicando conceptos avanzados de POO.

---

## 📐 Arquitectura POO Propuesta

### 1. HERENCIA - Plan de Cuentas Jerárquico

```
Cuenta (Clase Base Abstracta)
├── Activo
│   ├── ActivoCorriente
│   │   ├── Efectivo
│   │   ├── CuentasPorCobrar
│   │   └── Inventario
│   └── ActivoNoCorriente
│       ├── PropiedadPlantaEquipo
│       └── ActivosIntangibles
├── Pasivo
│   ├── PasivoCorriente
│   │   ├── CuentasPorPagar
│   │   └── DeudaCortoplazo
│   └── PasivoNoCorriente
│       └── DeudaLargoPlazo
├── Patrimonio
│   ├── Capital
│   └── UtilidadesRetenidas
├── Ingreso
│   ├── IngresoOperacional
│   └── IngresoNoOperacional
└── Gasto
    ├── GastoOperacional
    └── GastoNoOperacional
```

### 2. POLIMORFISMO - Comportamiento por Tipo de Cuenta

```python
class Cuenta(ABC):
    @abstractmethod
    def registrar_movimiento(self, monto, tipo):
        pass
    
    @abstractmethod
    def calcular_saldo(self):
        pass

class Activo(Cuenta):
    def registrar_movimiento(self, monto, tipo):
        # Activo aumenta con DÉBITO
        if tipo == 'DEBITO':
            self.saldo += monto
        else:
            self.saldo -= monto

class Pasivo(Cuenta):
    def registrar_movimiento(self, monto, tipo):
        # Pasivo aumenta con CRÉDITO
        if tipo == 'CREDITO':
            self.saldo += monto
        else:
            self.saldo -= monto
```

### 3. ENCAPSULAMIENTO - Lógica de Negocio en Modelos

```python
class AsientoContable(models.Model):
    # Atributos privados (protegidos)
    _fecha = models.DateField()
    _descripcion = models.TextField()
    
    # Método público que encapsula lógica
    def esta_balanceado(self):
        total_debitos = self.movimientos.aggregate(
            total=Sum('debito')
        )['total'] or 0
        
        total_creditos = self.movimientos.aggregate(
            total=Sum('credito')
        )['total'] or 0
        
        return total_debitos == total_creditos
    
    def save(self, *args, **kwargs):
        # Validación encapsulada
        if not self.esta_balanceado():
            raise ValidationError("El asiento debe estar balanceado")
        super().save(*args, **kwargs)
```

### 4. ABSTRACCIÓN - Interfaces Claras

```python
class DocumentoContable(ABC):
    @abstractmethod
    def generar_asiento(self):
        """Cada documento genera su asiento de forma diferente"""
        pass
    
    @abstractmethod
    def validar(self):
        """Cada documento tiene sus propias reglas de validación"""
        pass

class Factura(DocumentoContable):
    def generar_asiento(self):
        # Lógica específica para facturas
        # Débito: Cuentas por Cobrar
        # Crédito: Ingresos
        pass

class NotaDeCredito(DocumentoContable):
    def generar_asiento(self):
        # Lógica específica para notas de crédito
        # Débito: Devoluciones
        # Crédito: Cuentas por Cobrar
        pass
```

### 5. COMPOSICIÓN - Objetos Compuestos

```python
class AsientoContable:
    # Un asiento está COMPUESTO por múltiples movimientos
    movimientos = models.ManyToManyField(Movimiento)
    
class Factura:
    # Una factura está COMPUESTA por múltiples items
    items = models.ManyToManyField(ItemFactura)
    
    def calcular_total(self):
        return sum(item.subtotal() for item in self.items.all())
```

---

## 🗂️ Estructura de Módulos

### Módulo 1: Plan de Cuentas
```
accounting/
├── models/
│   ├── cuenta_base.py          # Clase abstracta Cuenta
│   ├── activo.py               # Herencia: Activo y subclases
│   ├── pasivo.py               # Herencia: Pasivo y subclases
│   ├── patrimonio.py           # Herencia: Patrimonio
│   ├── ingreso.py              # Herencia: Ingreso
│   └── gasto.py                # Herencia: Gasto
├── views/
│   ├── plan_cuentas_views.py   # CRUD del plan de cuentas
│   └── jerarquia_views.py      # Visualización jerárquica
└── templates/
    └── plan_cuentas/
```

### Módulo 2: Asientos Contables (Libro Diario)
```
accounting/
├── models/
│   ├── asiento_contable.py     # Encapsulamiento: validación
│   ├── movimiento.py           # Débitos y créditos
│   └── libro_diario.py         # Agregación de asientos
├── views/
│   ├── asiento_views.py        # Crear/editar asientos
│   └── libro_diario_views.py   # Visualizar libro diario
└── templates/
    └── asientos/
```

### Módulo 3: Documentos Contables
```
accounting/
├── models/
│   ├── documento_base.py       # Clase abstracta
│   ├── factura.py              # Polimorfismo: generar_asiento()
│   ├── nota_credito.py         # Polimorfismo: generar_asiento()
│   └── recibo.py               # Polimorfismo: generar_asiento()
└── views/
    └── documentos_views.py
```

### Módulo 4: Reportes Financieros
```
accounting/
├── reports/
│   ├── balance_comprobacion.py # Suma débitos/créditos
│   ├── estado_resultados.py    # Ingresos - Gastos
│   └── balance_general.py      # Activos = Pasivos + Patrimonio
├── views/
│   └── reportes_views.py
└── templates/
    └── reportes/
```

---

## 📋 Modelos Principales

### 1. Cuenta (Base Abstracta)
```python
from abc import ABC, abstractmethod

class CuentaBase(models.Model, ABC):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cuenta_padre = models.ForeignKey('self', null=True, blank=True)
    nivel = models.IntegerField(default=1)
    naturaleza = models.CharField(
        max_length=10,
        choices=[('DEUDORA', 'Deudora'), ('ACREEDORA', 'Acreedora')]
    )
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    class Meta:
        abstract = True
    
    @abstractmethod
    def registrar_movimiento(self, monto, tipo):
        pass
    
    @abstractmethod
    def calcular_saldo(self):
        pass
    
    def obtener_jerarquia(self):
        """Retorna la ruta completa de la cuenta"""
        if self.cuenta_padre:
            return f"{self.cuenta_padre.obtener_jerarquia()} > {self.nombre}"
        return self.nombre
```

### 2. AsientoContable (Encapsulamiento)
```python
class AsientoContable(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('BORRADOR', 'Borrador'),
            ('REGISTRADO', 'Registrado'),
            ('ANULADO', 'Anulado')
        ],
        default='BORRADOR'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def esta_balanceado(self):
        """Encapsulamiento: lógica de validación"""
        total_debitos = self.movimientos.aggregate(
            total=Sum('debito')
        )['total'] or Decimal('0')
        
        total_creditos = self.movimientos.aggregate(
            total=Sum('credito')
        )['total'] or Decimal('0')
        
        return total_debitos == total_creditos
    
    def registrar(self):
        """Encapsulamiento: proceso de registro"""
        if not self.esta_balanceado():
            raise ValidationError("El asiento debe estar balanceado")
        
        if self.estado != 'BORRADOR':
            raise ValidationError("Solo se pueden registrar asientos en borrador")
        
        # Aplicar movimientos a las cuentas
        for movimiento in self.movimientos.all():
            movimiento.aplicar()
        
        self.estado = 'REGISTRADO'
        self.save()
    
    def anular(self):
        """Encapsulamiento: proceso de anulación"""
        if self.estado != 'REGISTRADO':
            raise ValidationError("Solo se pueden anular asientos registrados")
        
        # Revertir movimientos
        for movimiento in self.movimientos.all():
            movimiento.revertir()
        
        self.estado = 'ANULADO'
        self.save()
```

### 3. Movimiento (Composición)
```python
class Movimiento(models.Model):
    asiento = models.ForeignKey(
        AsientoContable,
        related_name='movimientos',
        on_delete=models.CASCADE
    )
    cuenta = models.ForeignKey('Cuenta', on_delete=models.PROTECT)
    debito = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credito = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200, blank=True)
    
    def aplicar(self):
        """Aplica el movimiento a la cuenta"""
        if self.debito > 0:
            self.cuenta.registrar_movimiento(self.debito, 'DEBITO')
        if self.credito > 0:
            self.cuenta.registrar_movimiento(self.credito, 'CREDITO')
    
    def revertir(self):
        """Revierte el movimiento de la cuenta"""
        if self.debito > 0:
            self.cuenta.registrar_movimiento(self.debito, 'CREDITO')
        if self.credito > 0:
            self.cuenta.registrar_movimiento(self.credito, 'DEBITO')
    
    def clean(self):
        """Validación: no puede tener débito y crédito al mismo tiempo"""
        if self.debito > 0 and self.credito > 0:
            raise ValidationError(
                "Un movimiento no puede tener débito y crédito simultáneamente"
            )
```

---

## 🎨 Funcionalidades Principales

### 1. Plan de Cuentas
- ✅ CRUD completo de cuentas
- ✅ Visualización jerárquica (árbol)
- ✅ Búsqueda y filtrado
- ✅ Importación/exportación

### 2. Asientos Contables
- ✅ Crear asientos con múltiples movimientos
- ✅ Validación automática de balance
- ✅ Estados: Borrador → Registrado → Anulado
- ✅ Libro diario completo

### 3. Reportes Financieros
- ✅ Balance de Comprobación
- ✅ Estado de Resultados
- ✅ Balance General
- ✅ Filtros por fecha
- ✅ Exportación a PDF/Excel

---

## 🚀 Plan de Implementación

### Fase 1: Refactorizar Modelos Actuales (2-3 días)
1. Crear estructura de herencia para Cuenta
2. Implementar clases Activo, Pasivo, Patrimonio, Ingreso, Gasto
3. Migrar datos actuales al nuevo modelo

### Fase 2: Asientos Contables (3-4 días)
1. Crear modelos AsientoContable y Movimiento
2. Implementar validación de balance
3. Crear interfaz para registro de asientos
4. Implementar libro diario

### Fase 3: Documentos Contables (2-3 días)
1. Crear clase abstracta DocumentoContable
2. Implementar Factura, NotaDeCredito, Recibo
3. Generar asientos automáticamente

### Fase 4: Reportes Financieros (3-4 días)
1. Balance de Comprobación
2. Estado de Resultados
3. Balance General
4. Exportación a PDF

### Fase 5: Pruebas y Refinamiento (2 días)
1. Pruebas unitarias
2. Pruebas de integración
3. Documentación

**Tiempo Total Estimado: 12-16 días**

---

## 📊 Ejemplo de Uso

### Crear un Asiento Contable

```python
# 1. Crear el asiento
asiento = AsientoContable.objects.create(
    numero='AS-001',
    fecha=date.today(),
    descripcion='Venta de mercancía',
    usuario=request.user
)

# 2. Agregar movimientos (Composición)
Movimiento.objects.create(
    asiento=asiento,
    cuenta=cuentas_por_cobrar,  # Activo (aumenta con débito)
    debito=1000,
    descripcion='Cliente Juan Pérez'
)

Movimiento.objects.create(
    asiento=asiento,
    cuenta=ingresos_ventas,  # Ingreso (aumenta con crédito)
    credito=1000,
    descripcion='Venta de productos'
)

# 3. Validar y registrar (Encapsulamiento)
if asiento.esta_balanceado():
    asiento.registrar()  # Aplica los movimientos
else:
    print("Error: El asiento no está balanceado")
```

### Generar Reporte

```python
# Estado de Resultados (Polimorfismo)
ingresos = Ingreso.objects.all()
gastos = Gasto.objects.all()

total_ingresos = sum(cuenta.calcular_saldo() for cuenta in ingresos)
total_gastos = sum(cuenta.calcular_saldo() for cuenta in gastos)

utilidad = total_ingresos - total_gastos
```

---

## ✅ Conceptos POO Aplicados

| Concepto | Dónde se Aplica |
|---|---|
| **Herencia** | Plan de Cuentas (Cuenta → Activo → ActivoCorriente) |
| **Polimorfismo** | registrar_movimiento() se comporta diferente por tipo |
| **Encapsulamiento** | AsientoContable.esta_balanceado(), .registrar() |
| **Abstracción** | DocumentoContable (clase abstracta) |
| **Composición** | AsientoContable compuesto por Movimientos |

---

## 🎯 Resultado Final

Un sistema completo de contabilidad que:
- ✅ Aplica todos los conceptos de POO requeridos
- ✅ Cumple con principios contables (partida doble)
- ✅ Genera reportes financieros estándar
- ✅ Es escalable y mantenible
- ✅ Tiene validaciones robustas

---

¿Quieres que comience con la implementación? Puedo empezar por cualquier fase que prefieras.

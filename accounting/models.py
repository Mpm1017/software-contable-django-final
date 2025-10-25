"""
Modelos del Sistema de Contabilidad
Importa todos los modelos desde el paquete models/
"""

# Importar todos los modelos nuevos (POO)
from .models.cuenta_base import CuentaContable
from .models.activo import Activo, ActivoCorriente, ActivoNoCorriente
from .models.pasivo import Pasivo, PasivoCorriente, PasivoNoCorriente
from .models.patrimonio import Patrimonio
from .models.ingreso import Ingreso
from .models.gasto import Gasto
from .models.asiento_contable import AsientoContable, Movimiento

# Importar modelos legacy para compatibilidad
from .models.legacy import Account, Category, Transaction

# Exportar todos los modelos
__all__ = [
    # Nuevos modelos POO
    'CuentaContable',
    'Activo', 'ActivoCorriente', 'ActivoNoCorriente',
    'Pasivo', 'PasivoCorriente', 'PasivoNoCorriente',
    'Patrimonio',
    'Ingreso',
    'Gasto',
    'AsientoContable',
    'Movimiento',
    # Modelos legacy
    'Account',
    'Category',
    'Transaction',
]

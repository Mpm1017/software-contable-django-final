"""Utilidades para el módulo de contabilidad"""
from .models import Category


# Categorías predeterminadas que se crearán para cada nuevo usuario
CATEGORIAS_PREDETERMINADAS = {
    'INCOME': [
        {'name': 'Salario', 'description': 'Ingreso por salario mensual', 'color': '#28a745'},
        {'name': 'Freelance', 'description': 'Ingresos por trabajos independientes', 'color': '#20c997'},
        {'name': 'Inversiones', 'description': 'Rendimientos de inversiones', 'color': '#17a2b8'},
        {'name': 'Ventas', 'description': 'Ingresos por ventas de productos o servicios', 'color': '#6610f2'},
        {'name': 'Otros Ingresos', 'description': 'Otros ingresos varios', 'color': '#6c757d'},
    ],
    'EXPENSE': [
        {'name': 'Alimentación', 'description': 'Gastos en comida y supermercado', 'color': '#fd7e14'},
        {'name': 'Transporte', 'description': 'Gastos en transporte y combustible', 'color': '#e83e8c'},
        {'name': 'Vivienda', 'description': 'Alquiler, servicios públicos, mantenimiento', 'color': '#dc3545'},
        {'name': 'Salud', 'description': 'Gastos médicos y medicamentos', 'color': '#d63384'},
        {'name': 'Educación', 'description': 'Gastos en educación y capacitación', 'color': '#6f42c1'},
        {'name': 'Entretenimiento', 'description': 'Ocio, cine, restaurantes', 'color': '#0dcaf0'},
        {'name': 'Ropa', 'description': 'Compra de ropa y accesorios', 'color': '#ffc107'},
        {'name': 'Tecnología', 'description': 'Gastos en tecnología y electrónicos', 'color': '#0d6efd'},
        {'name': 'Servicios', 'description': 'Internet, teléfono, suscripciones', 'color': '#198754'},
        {'name': 'Otros Gastos', 'description': 'Otros gastos varios', 'color': '#6c757d'},
    ]
}


def crear_categorias_predeterminadas(user):
    """
    Crea las categorías predeterminadas para un nuevo usuario.
    
    Args:
        user: Usuario de Django para el cual crear las categorías
    
    Returns:
        int: Número de categorías creadas
    """
    categorias_creadas = 0
    
    # Crear categorías de ingresos
    for cat_data in CATEGORIAS_PREDETERMINADAS['INCOME']:
        Category.objects.get_or_create(
            user=user,
            name=cat_data['name'],
            category_type='INCOME',
            defaults={
                'description': cat_data['description'],
                'color': cat_data['color'],
                'is_active': True
            }
        )
        categorias_creadas += 1
    
    # Crear categorías de gastos
    for cat_data in CATEGORIAS_PREDETERMINADAS['EXPENSE']:
        Category.objects.get_or_create(
            user=user,
            name=cat_data['name'],
            category_type='EXPENSE',
            defaults={
                'description': cat_data['description'],
                'color': cat_data['color'],
                'is_active': True
            }
        )
        categorias_creadas += 1
    
    return categorias_creadas


def obtener_categorias_con_predeterminadas(user, category_type=None):
    """
    Obtiene las categorías del usuario, asegurándose de que existan las predeterminadas.
    
    Args:
        user: Usuario de Django
        category_type: Tipo de categoría ('INCOME' o 'EXPENSE'), None para todas
    
    Returns:
        QuerySet: Categorías del usuario
    """
    # Verificar si el usuario tiene categorías
    if not Category.objects.filter(user=user).exists():
        crear_categorias_predeterminadas(user)
    
    # Retornar categorías filtradas
    queryset = Category.objects.filter(user=user, is_active=True)
    if category_type:
        queryset = queryset.filter(category_type=category_type)
    
    return queryset.order_by('category_type', 'name')